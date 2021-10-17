import 'package:flutter/material.dart';
import '../Auth/login_navigator.dart';
import '../BottomNavigation/Explore/more_page.dart';
import '../BottomNavigation/MyProfile/badge_request.dart';
import '../BottomNavigation/MyProfile/language_page.dart';
import '../BottomNavigation/MyProfile/video_option.dart';
import '../BottomNavigation/bottom_navigation.dart';
import '../BottomNavigation/AddVideo/add_video.dart';
import '../BottomNavigation/AddVideo/add_video_filter.dart';
import '../BottomNavigation/MyProfile/followers.dart';
import '../BottomNavigation/MyProfile/help_page.dart';
import '../BottomNavigation/AddVideo/post_info.dart';
import '../BottomNavigation/Explore/search_users.dart';
import '../BottomNavigation/MyProfile/tnc.dart';
// import '../Chat/chat_page.dart';
// import '../Screens/user_profile.dart';

class PageRoutes {
  static const String loginNavigator = 'login_navigator';
  static const String bottomNavigation = 'bottom_navigation';
  static const String followersPage = 'followers_page';
  static const String helpPage = 'help_page';
  static const String tncPage = 'tnc_page';
  static const String searchPage = 'search_page';
  static const String addVideoPage = 'add_video_page';
  static const String addVideoFilterPage = 'add_video_filter_page';
  static const String postInfoPage = 'post_info_page';
  static const String userProfilePage = 'user_profile_page';
  static const String chatPage = 'chat_page';
  static const String morePage = 'more_page';
  static const String videoOptionPage = 'video_option_page';
  static const String verifiedBadgePage = 'verified_badge_page';
  static const String languagePage = 'language_page';

  Map<String, WidgetBuilder> routes() {
    return {
      loginNavigator: (context) => LoginNavigator(),
      bottomNavigation: (context) => BottomNavigation(),
      followersPage: (context) => FollowersPage(),
      helpPage: (context) => HelpPage(),
      tncPage: (context) => TnC(),
      searchPage: (context) => SearchUsers(),
      addVideoPage: (context) => AddVideo(),
      addVideoFilterPage: (context) => AddVideoFilter(),
      postInfoPage: (context) => PostInfo(),
      // userProfilePage: (context) => UserProfilePage(),
      // chatPage: (context) => ChatPage(),
      morePage: (context) => MorePage(),
      videoOptionPage: (context) => VideoOptionPage(),
      verifiedBadgePage: (context) => BadgeRequest(),
      languagePage: (context) => ChangeLanguagePage(),
    };
  }
}
