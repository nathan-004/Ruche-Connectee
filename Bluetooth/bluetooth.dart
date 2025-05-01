import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';

// UUIDs for Nordic UART Service
final Guid UART_SERVICE_UUID = Guid("6E400001-B5A3-F393-E0A9-E50E24DCCA9E");
final Guid UART_TX_CHAR_UUID = Guid("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"); // Write
final Guid UART_RX_CHAR_UUID = Guid("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"); // Notify

class BluetoothScreen extends StatefulWidget {
  const BluetoothScreen({Key? key}) : super(key: key);

  @override
  State<BluetoothScreen> createState() => _BluetoothScreenState();
}

class _BluetoothScreenState extends State<BluetoothScreen> {
  final List<ScanResult> _devices = [];
  BluetoothDevice? _connectedDevice;
  BluetoothCharacteristic? _txCharacteristic;
  BluetoothCharacteristic? _rxCharacteristic;
  List<String> _received = [];

  @override
  void initState() {
    super.initState();
    _checkPermissions();
  }

  Future<void> _checkPermissions() async {
    await Permission.bluetooth.request();
    await Permission.bluetoothScan.request();
    await Permission.bluetoothConnect.request();
    await Permission.location.request();
  }

  Future<void> _startScan() async {
    _devices.clear();
    setState(() {});
    await FlutterBluePlus.startScan(timeout: const Duration(seconds: 5));
    FlutterBluePlus.scanResults.listen((results) {
      for (var r in results) {
        if (!_devices.any((d) => d.device.id == r.device.id)) {
          _devices.add(r);
        }
      }
      setState(() {});
    });
    await Future.delayed(const Duration(seconds: 5));
    await FlutterBluePlus.stopScan();
  }

  Future<void> _connect(ScanResult r) async {
    final device = r.device;
    await device.connect();
    _connectedDevice = device;
    final services = await device.discoverServices();
    for (var svc in services) {
      if (svc.uuid == UART_SERVICE_UUID) {
        for (var c in svc.characteristics) {
          if (c.uuid == UART_TX_CHAR_UUID) {
            _txCharacteristic = c;
          } else if (c.uuid == UART_RX_CHAR_UUID) {
            _rxCharacteristic = c;
            await _rxCharacteristic!.setNotifyValue(true);
            _rxCharacteristic!.value.listen((data) {
              final msg = String.fromCharCodes(data);
              setState(() => _received.add(msg));
            });
          }
        }
      }
    }
    setState(() {});
  }

  Future<void> _sendMessage(String msg) async {
    if (_txCharacteristic != null) {
      await _txCharacteristic!.write(msg.codeUnits, withoutResponse: true);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bluetooth UART'),
      ),
      body: _connectedDevice == null
          ? Column(
        children: [
          ElevatedButton(
            onPressed: _startScan,
            child: const Text('Scan Devices'),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _devices.length,
              itemBuilder: (context, i) {
                final d = _devices[i];
                return ListTile(
                  title: Text(
                      d.device.name.isNotEmpty ? d.device.name : d.device.id.toString()),
                  subtitle: Text(d.rssi.toString() + ' dBm'),
                  trailing: ElevatedButton(
                    child: const Text('Connect'),
                    onPressed: () => _connect(d),
                  ),
                );
              },
            ),
          ),
        ],
      )
          : _buildChat(),
    );
  }

  Widget _buildChat() {
    final deviceName = _connectedDevice!.name.isEmpty
        ? _connectedDevice!.id.toString()
        : _connectedDevice!.name;
    final textController = TextEditingController();
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text('Connected to $deviceName'),
        ),
        Expanded(
          child: ListView(
            children: _received.map((s) => ListTile(title: Text(s))).toList(),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  controller: textController,
                  decoration: const InputDecoration(
                    hintText: 'Enter message',
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.send),
                onPressed: () => _sendMessage(textController.text),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
