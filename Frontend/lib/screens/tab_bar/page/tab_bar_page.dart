import 'package:fitness_flutter/core/const/color_constants.dart';
import 'package:fitness_flutter/core/const/path_constants.dart';
import 'package:fitness_flutter/core/const/text_constants.dart';
import 'package:fitness_flutter/screens/home/page/home_page.dart';
import 'package:fitness_flutter/screens/reels/page/notification_messages.dart';
import 'package:fitness_flutter/screens/reels/page/chat_page.dart';
import 'package:fitness_flutter/screens/settings/settings_screen.dart';
import 'package:fitness_flutter/screens/tab_bar/bloc/tab_bar_bloc.dart';
import 'package:fitness_flutter/screens/reels/page/home_page.dart';
import 'package:fitness_flutter/screens/workouts/page/workouts_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class TabBarPage extends StatelessWidget {
  const TabBarPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocProvider<TabBarBloc>(
      create: (BuildContext context) => TabBarBloc(),
      child: BlocConsumer<TabBarBloc, TabBarState>(
        listener: (context, state) {},
        buildWhen: (_, currState) =>
            currState is TabBarInitial || currState is TabBarItemSelectedState,
        builder: (context, state) {
          final bloc = BlocProvider.of<TabBarBloc>(context);
          return Scaffold(
            body: _createBody(context, bloc.currentIndex),
            bottomNavigationBar: _createdBottomTabBar(context),
          );
        },
      ),
    );
  }

  Widget _createdBottomTabBar(BuildContext context) {
    final bloc = BlocProvider.of<TabBarBloc>(context);
    return BottomNavigationBar(
      currentIndex: bloc.currentIndex,
      fixedColor: ColorConstants.primaryColor,
      items: [
        BottomNavigationBarItem(
          icon: Image(
            image: AssetImage(PathConstants.reel),
            width: 20,
            height: 20,
            color: bloc.currentIndex == 0
                ? ColorConstants.primaryColor
                : Colors.grey,
          ),
          label: TextConstants.reel,
        ),
        BottomNavigationBarItem(
          icon: Image(
            image: AssetImage(PathConstants.chat),
            width: 20,
            height: 20,
            color: bloc.currentIndex == 1
                ? ColorConstants.primaryColor
                : Colors.grey,
          ),
          label: TextConstants.chats,
        ),
        BottomNavigationBarItem(
          icon: Image(
            image: AssetImage(PathConstants.explore),
            width: 20,
            height: 20,
            color: bloc.currentIndex == 2
                ? ColorConstants.primaryColor
                : Colors.grey,
          ),
          label: TextConstants.gymbuddy,
        ),
        BottomNavigationBarItem(
          icon: Image(
            image: AssetImage(PathConstants.workouts),
            width: 10,
            height: 10,
            color: bloc.currentIndex == 3
                ? ColorConstants.primaryColor
                : Colors.grey,
          ),
          label: TextConstants.workouts,
        ),
        BottomNavigationBarItem(
          icon: Image(
            image: AssetImage(PathConstants.profile),
            width: 20,
            height: 20,
            color: bloc.currentIndex == 4 ? ColorConstants.primaryColor : null,
          ),
          label: TextConstants.profile,
        ),
      ],
      onTap: (index) {
        bloc.add(TabBarItemTappedEvent(index: index));
      },
    );
  }

  Widget _createBody(BuildContext context, int index) {
    final children = [
      HomeBody(),
      NotificationMessages(),
      WorkoutsPage(),
      HomePage(),
      SettingsScreen(),

      // Scaffold(
      //   body: Center(
      //     child: RawMaterialButton(
      //       fillColor: Colors.red,
      //       child: Text(
      //         TextConstants.signOut,
      //         style: TextStyle(
      //           color: ColorConstants.white,
      //         ),
      //       ),
      //       onPressed: () {
      //         AuthService.signOut();
      //         Navigator.pushReplacement(
      //           context,
      //           MaterialPageRoute(builder: (_) => SignInPage()),
      //         );
      //       },
      //     ),
      //   ),
      // ),
    ];
    return children[index];
  }
}
