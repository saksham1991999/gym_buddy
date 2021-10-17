import 'package:flutter/material.dart';
import 'dart:async';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ExplorePage extends StatefulWidget {
  const ExplorePage({Key? key}) : super(key: key);

  @override
  _ExplorePageState createState() => _ExplorePageState();
}

class _ExplorePageState extends State<ExplorePage> {
  Completer<GoogleMapController> _controller = Completer();

  static const LatLng _center = const LatLng(28.445974, 77.00829400000001);
  @override
  void initState() {
    // TODO: implement initState
    getNearbyHunks();
    super.initState();
  }

  void _onMapCreated(GoogleMapController controller) {
    _controller.complete(controller);
  }

  final Set<Marker> markers = new Set(); //markers for google map
  // static const LatLng showLocation = const LatLng(28.445974, 77.00829400000001);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: users.length == 0
          ? Container(
              alignment: Alignment.center,
              height: MediaQuery.of(context).size.height,
              width: MediaQuery.of(context).size.width,
              child: Text("Fetching Info...."))
          : Stack(
              children: [
                GoogleMap(
                  onMapCreated: _onMapCreated,
                  initialCameraPosition: CameraPosition(
                    target: _center,
                    zoom: 11.0,
                  ),
                  markers: markers,
                ),
                Positioned(
                  bottom: 0,
                  child: InkWell(
                    onTap: () {
                      showModalBottomSheet<void>(
                        context: context,
                        builder: (BuildContext context) {
                          return Container(
                            height: MediaQuery.of(context).size.height,
                            decoration: BoxDecoration(
                              // borderRadius: BorderRadius.only(topLeft: Radius.circular(15),topRight: Radius.circular(15)),
                              color: Colors.amber,
                            ),
                            child: Center(
                              child: Column(
                                children: [
                                  Padding(
                                    padding: const EdgeInsets.all(10.0),
                                    child: Text("Find a Buddy Nearby!"),
                                  ),
                                  Container(
                                    height: MediaQuery.of(context).size.height *
                                        0.5,
                                    child: ListView(
                                      children:
                                          List.generate(users.length, (i) {
                                        return Card(
                                          child: ListTile(
                                            leading: Image(
                                              image: NetworkImage(
                                                  users[i]["profile_pic"],
                                                  scale: 2),
                                            ),
                                            title: Text(users[i]["first_name"] +
                                                " " +
                                                users[i]["last_name"]),
                                            subtitle: Text(
                                                "Distance: ${users[i]["distance"]}"),
                                            trailing: Icon(Icons.more_vert),
                                          ),
                                        );
                                      }),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      );
                    },
                    child: Container(
                        alignment: Alignment.center,
                        height: 40,
                        decoration: BoxDecoration(
                          color: Colors.grey.shade400.withOpacity(0.5),
                        ),
                        width: MediaQuery.of(context).size.width,
                        child: Row(
                          children: [
                            Icon(
                              Icons.arrow_circle_up,
                            ),
                            SizedBox(width: 20),
                            Text("Find Your Nearby Gym Buddy",
                                style: TextStyle(
                                    color: Colors.black, fontSize: 15)),
                          ],
                        )),
                  ),
                ),
                Positioned(
                  top: 20,
                  child: Container(
                      height: 50,
                      width: MediaQuery.of(context).size.width,
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              alignment: Alignment.center,
                              height: 40,
                              width: MediaQuery.of(context).size.width / 3 - 20,
                              decoration: BoxDecoration(
                                borderRadius:
                                    BorderRadius.all(Radius.circular(20)),
                                color: Colors.blue.shade200.withOpacity(0.7),
                              ),
                              child: Text("Buddy"),
                            ),
                            SizedBox(width: 15),
                            Container(
                              alignment: Alignment.center,
                              height: 40,
                              width: MediaQuery.of(context).size.width / 3 - 20,
                              decoration: BoxDecoration(
                                  borderRadius:
                                      BorderRadius.all(Radius.circular(20)),
                                  color: Colors.black.withOpacity(0.3)),
                              child: Text("Trainer"),
                            ),
                            SizedBox(width: 15),
                            Container(
                              alignment: Alignment.center,
                              height: 40,
                              width: MediaQuery.of(context).size.width / 3 - 20,
                              decoration: BoxDecoration(
                                  borderRadius:
                                      BorderRadius.all(Radius.circular(20)),
                                  color: Colors.black.withOpacity(0.3)),
                              child: Text("Professionals"),
                            )
                          ])),
                )
              ],
            ),
    );
  }

  var users = [];

  getNearbyHunks() async {
    final response = await http.get(
        Uri.parse(
            'https://78b9-171-78-227-21.ngrok.io/accounts/users/?latitude=28.445974&longitude=77.00829400000001&type=U'),
        headers: {
          'Authorization': "Token 3230a41b20f139f8e4ed2ffcd2a68d2200566a71"
        });

    var data = jsonDecode(response.body);
    if (data != null || data["results"] != null) {
      setState(() {
        users = data["results"];
      });
      print(users);
      getmarkers();
    }
  }

  Set<Marker> getmarkers() {
    setState(() {
      for (int i = 0; i < users.length; i++) {
        markers.add(Marker(
          //add second marker
          markerId: MarkerId(
              LatLng(users[i]['latitude'], users[i]["longitude"]).toString()),
          position: LatLng(
              users[i]['longitude'], users[i]["latitude"]), //position of marker
          infoWindow: InfoWindow(
            //popup info
            title: users[i]["first_name"],
            snippet: users[i]["distance"],
          ),
          icon: BitmapDescriptor.defaultMarker, //Icon for Marker
        ));
      }
    });
    print(markers);
    print("********************************************");

    return markers;
  }
}
