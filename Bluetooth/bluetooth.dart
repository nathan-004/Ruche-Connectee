import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:convert';  // pour utf8

// UUIDs for Nordic UART Service
final Guid UART_SERVICE_UUID    = Guid("6E400001-B5A3-F393-E0A9-E50E24DCCA9E");
final Guid UART_RX_CHAR_UUID    = Guid("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"); // Write from app
final Guid UART_TX_CHAR_UUID    = Guid("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"); // Notify to app

class BluetoothScreen extends StatefulWidget {
  const BluetoothScreen({Key? key}) : super(key: key);
  @override
  State<BluetoothScreen> createState() => _BluetoothScreenState();
}

class _BluetoothScreenState extends State<BluetoothScreen> {
  final List<ScanResult> _devices = [];
  BluetoothDevice? _connectedDevice;
  BluetoothCharacteristic? _rxChar, _txChar;
  final List<String> _received = [];
  final TextEditingController _textCtrl = TextEditingController();

  String _rxBuffer = "";

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
    FlutterBluePlus.scanResults.listen((rList) {
      for (var r in rList) {
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
    try {
      await r.device.connect();
      _connectedDevice = r.device;
      final services = await r.device.discoverServices();
      for (var s in services) {
        if (s.uuid == UART_SERVICE_UUID) {
          for (var c in s.characteristics) {
            if (c.uuid == UART_RX_CHAR_UUID) {
              _rxChar = c;
            }
            else if (c.uuid == UART_TX_CHAR_UUID) {
              _txChar = c;
              await c.setNotifyValue(true);
              c.value.listen(_onData);
            }
          }
        }
      }
      setState(() {});
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Erreur de connexion: $e"))
      );
    }
  }

  void _onData(List<int> data) {
    // Concatène et découpe selon '#'
    _rxBuffer += utf8.decode(data);
    var parts = _rxBuffer.split('#');
    for (var i = 0; i < parts.length - 1; i++) {
      setState(() => _received.add(parts[i]));
    }
    _rxBuffer = parts.last;
  }

  Future<void> _sendMessage() async {
    final msg = _textCtrl.text.trim();
    if (_txChar == null || _connectedDevice == null) {
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Pas de connexion établie"))
      );
      return;
    }
    final full = msg + "#";
    try {
      // write WITH response (default)
      await _txChar!.write(utf8.encode(full));
      _textCtrl.clear();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Erreur envoi: $e"))
      );
    }
  }

  @override
  void dispose() {
    _textCtrl.dispose();
    _connectedDevice?.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Bluetooth UART")),
      body: _connectedDevice == null
          ? _buildScanner()
          : _buildChat(),
    );
  }

  Widget _buildScanner() {
    return Column(
      children: [
        ElevatedButton(
          onPressed: _startScan,
          child: const Text("Scanner BLE"),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: _devices.length,
            itemBuilder: (_, i) {
              final d = _devices[i];
              return ListTile(
                title: Text(d.device.name.isNotEmpty
                    ? d.device.name
                    : d.device.id.toString()
                ),
                subtitle: Text("${d.rssi} dBm"),
                trailing: ElevatedButton(
                  onPressed: () => _connect(d),
                  child: const Text("Connecter"),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildChat() {
    final name = _connectedDevice!.name.isNotEmpty
        ? _connectedDevice!.name
        : _connectedDevice!.id.toString();
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text("Connecté à $name"),
        ),
        Expanded(
          child: ListView(
            children: _received
                .map((s) => ListTile(title: Text(s)))
                .toList(),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _textCtrl,
                  decoration: const InputDecoration(
                    hintText: "Message",
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.send),
                onPressed: _sendMessage,
              ),
            ],
          ),
        ),
      ],
    );
  }
}
