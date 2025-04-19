import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ruche Connectée',
      theme: ThemeData(
        primarySwatch: Colors.amber,
        scaffoldBackgroundColor: Colors.yellow[50],
      ),
      home: BeehiveHomePage(),
    );
  }
}

class BeehiveHomePage extends StatefulWidget {
  @override
  _BeehiveHomePageState createState() => _BeehiveHomePageState();
}

class _BeehiveHomePageState extends State<BeehiveHomePage> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    OverviewPage(),
    GraphsPage(),
    SettingsPage(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Ruche Connectée'),
      ),
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        selectedItemColor: Colors.amber[800],
        items: const [
          BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: "Vue d'ensemble",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.show_chart),
            label: 'Graphiques',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: 'Paramètres',
          ),
        ],
      ),
    );
  }
}

class OverviewPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          Container(
            width: double.infinity,
            height: 150,
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/beehive_banner.jpg"),
                fit: BoxFit.cover,
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                MetricCard(label: 'Température', value: '35°C'),
                MetricCard(label: 'Humidité', value: '60%'),
                MetricCard(label: 'Poids', value: '2.5kg'),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: WeatherWidget(),
          ),
        ],
      ),
    );
  }
}

class GraphsPage extends StatelessWidget {
  final List<FlSpot> weightData = List.generate(
      10, (index) => FlSpot(index.toDouble(), (2 + index * 0.1)));
  final List<FlSpot> temperatureData = List.generate(
      10, (index) => FlSpot(index.toDouble(), (30 + index).toDouble()));
  final List<FlSpot> humidityData = List.generate(
      10, (index) => FlSpot(index.toDouble(), (50 + index).toDouble()));

  Widget buildGraph(String title, List<FlSpot> data) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16.0, horizontal: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          SizedBox(
            height: 200,
            child: LineChart(
              LineChartData(
                titlesData: FlTitlesData(
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(showTitles: true),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(showTitles: true),
                  ),
                ),
                borderData: FlBorderData(show: false),
                lineBarsData: [
                  LineChartBarData(
                    isCurved: true,
                    spots: data,
                    barWidth: 3,
                    color: Colors.amber,
                    belowBarData: BarAreaData(show: false),
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        buildGraph("Poids de la ruche", weightData),
        buildGraph("Température", temperatureData),
        buildGraph("Humidité", humidityData),
      ],
    );
  }
}

class SettingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: [
        ListTile(
          title: Text("Intervalle d'envoi de données"),
          subtitle: Text("30 minutes"),
          trailing: Icon(Icons.edit),
        ),
        Divider(),
        ListTile(
          title: Text("Localisation de la ruche"),
          subtitle: Text("Jardin arrière - Latitude: 46.5, Longitude: 0.3"),
          trailing: Icon(Icons.location_on),
        ),
        Divider(),
        ListTile(
          title: Text("Seuils d'alerte"),
          subtitle: Text("Température > 40°C, Humidité < 40%"),
          trailing: Icon(Icons.warning),
        ),
      ],
    );
  }
}

class MetricCard extends StatelessWidget {
  final String label;
  final String value;

  MetricCard({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          label,
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
        SizedBox(height: 8),
        Text(
          value,
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
}

class WeatherWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: Colors.amber[100],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Icon(Icons.wb_sunny, size: 40, color: Colors.orange),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("Soleil", style: TextStyle(fontSize: 18)),
              Text("25°C, Vent léger", style: TextStyle(fontSize: 14)),
            ],
          )
        ],
      ),
    );
  }
}
