import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:open_meteo/open_meteo.dart';

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
            child: WeatherWidget(latitude: 48.8566, longitude: 2.3522),
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
class WeatherWidget extends StatefulWidget {
  final double latitude;
  final double longitude;

  const WeatherWidget({
    super.key,
    required this.latitude,
    required this.longitude,
  });

  @override
  State<WeatherWidget> createState() => _WeatherWidgetState();
}

class _WeatherWidgetState extends State<WeatherWidget> {
  late final Future<ApiResponse<WeatherApi>> _weatherFuture;

  @override
  void initState() {
    super.initState();

    // Préparer la requête : on demande 3 variables horaires
    _weatherFuture = WeatherApi(temperatureUnit: TemperatureUnit.celsius, precipitationUnit: PrecipitationUnit.mm, windspeedUnit: WindspeedUnit.kmh).request(
      latitude: widget.latitude,
      longitude: widget.longitude,

      // On récupère les séries horaires suivantes
      hourly: {
        WeatherHourly.temperature_2m,     // Température en °C
        WeatherHourly.precipitation,     // Précipitations en mm
        WeatherHourly.wind_speed_10m,     // Vent à 10 m en km/h
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<ApiResponse<WeatherApi>>(
      future: _weatherFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          // En cours de chargement
          print("Still loading… state = ${snapshot.connectionState}");
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError || snapshot.data == null) {
          // En cas d’erreur
          print("Error: ${snapshot.error}");
          return const Center(child: Text("Impossible de charger la météo"));
        }

        final response = snapshot.data!;
        final hourly = response.hourlyData;
        // ignore: avoid_print
        print(hourly.toString());

        // On prend la première valeur de chaque série horaire
        final tempsList = hourly[WeatherHourly.temperature_2m]!;
        final precsList = hourly[WeatherHourly.precipitation]!;
        final windList = hourly[WeatherHourly.wind_speed_10m]!;

        final tempsValues = tempsList.values.entries.map((e) => e.value).toList();
        final num temp = tempsValues.isNotEmpty ? tempsValues[0] : 0.0;

        final precipValues = precsList.values.entries.map((e) => e.value).toList();
        final num precip = precipValues.isNotEmpty ? precipValues[0] : 0.0;

        final windValues = windList.values.entries.map((e) => e.value).toList();
        final num wind = windValues.isNotEmpty ? windValues[0] : 0.0;

        final bool isRaining = precip > 0.0;

        return Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.amber[100],
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Icon(
                isRaining ? Icons.cloud : Icons.wb_sunny,
                size: 40,
                color: isRaining ? Colors.blue : Colors.orange,
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    isRaining ? "Pluie" : "Ensoleillé",
                    style: const TextStyle(fontSize: 18),
                  ),
                  Text(
                    "${temp.toStringAsFixed(1)}°C, Vent ${wind.toStringAsFixed(0)} km/h",
                    style: const TextStyle(fontSize: 14),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}
