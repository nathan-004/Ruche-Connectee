import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';

class BluetoothScreen extends StatefulWidget {
  const BluetoothScreen({Key? key}) : super(key: key);

  @override
  State<BluetoothScreen> createState() => _BluetoothScreenState();
}

class _BluetoothScreenState extends State<BluetoothScreen> {
  final List<ScanResult> _devices = [];

  Future<void> _startScan() async {
    // Demande les permissions (Bluetooth + localisation si nécessaire)
    await Permission.bluetooth.request();
    await Permission.location.request();
    await Permission.bluetoothScan.request();
    await Permission.bluetoothConnect.request();

    setState(() => _devices.clear());

    // Démarre le scan
    await FlutterBluePlus.startScan(timeout: const Duration(seconds: 5));

    // Écoute les résultats
    FlutterBluePlus.scanResults.listen((results) {
      for (ScanResult result in results) {
        if (!_devices.any((d) => d.device.id == result.device.id)) {
          setState(() => _devices.add(result));
        }
      }
    });

    // Stop automatique après 5 secondes
    await Future.delayed(const Duration(seconds: 5));
    await FlutterBluePlus.stopScan();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan Bluetooth')),
      body: Column(
        children: [
          ElevatedButton(
            onPressed: _startScan,
            child: const Text('Scanner'),
          ),
          const SizedBox(height: 20),
          Expanded(
            child: ListView.builder(
              itemCount: _devices.length,
              itemBuilder: (context, index) {
                final device = _devices[index].device;
                return ListTile(
                  title: Text(device.name.isEmpty ? 'Inconnu' : device.name),
                  subtitle: Text(device.id.toString()),
                  trailing: const Icon(Icons.bluetooth),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
