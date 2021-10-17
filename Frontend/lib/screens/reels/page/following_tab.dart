import 'package:chewie/chewie.dart';
import 'package:flutter/material.dart';
import '../Auth/login_navigator.dart';
import '../BottomNavigation/Home/comment_sheet.dart';
import '../Components/custom_button.dart';
import '../Components/rotated_image.dart';
import '../../Locale/locale.dart';
import '../Routes/routes.dart';
import '../../Theme/colors.dart';
import 'package:video_player/video_player.dart';

RouteObserver<PageRoute> routeObserver = RouteObserver<PageRoute>();

class FollowingTabPage extends StatelessWidget {
  final List<String> videos;
  final List<String> images;
  final bool isFollowing;

  final int? variable;

  FollowingTabPage(this.videos, this.images, this.isFollowing, {this.variable});

  @override
  Widget build(BuildContext context) {
    return FollowingTabBody(videos, images, isFollowing, variable);
  }
}

class FollowingTabBody extends StatefulWidget {
  final List<String> videos;
  final List<String> images;

  final bool isFollowing;
  final int? variable;

  FollowingTabBody(this.videos, this.images, this.isFollowing, this.variable);

  @override
  _FollowingTabBodyState createState() => _FollowingTabBodyState();
}

class _FollowingTabBodyState extends State<FollowingTabBody> {
  PageController? _pageController;
  int current = 0;
  bool isOnPageTurning = false;

  void scrollListener() {
    if (isOnPageTurning &&
        _pageController!.page == _pageController!.page!.roundToDouble()) {
      setState(() {
        current = _pageController!.page!.toInt();
        isOnPageTurning = false;
      });
    } else if (!isOnPageTurning &&
        current.toDouble() != _pageController!.page) {
      if ((current.toDouble() - _pageController!.page!).abs() > 0.1) {
        setState(() {
          isOnPageTurning = true;
        });
      }
    }
  }

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _pageController!.addListener(scrollListener);
  }

  @override
  Widget build(BuildContext context) {
    return PageView.builder(
      physics: BouncingScrollPhysics(),
      scrollDirection: Axis.vertical,
      controller: _pageController,
      itemBuilder: (context, position) {
        return VideoPage(
          widget.videos[position],
          widget.images[position],
          pageIndex: position,
          currentPageIndex: current,
          isPaused: isOnPageTurning,
          isFollowing: widget.isFollowing,
        );
      },
      onPageChanged: widget.variable == null
          ? (i) async {
              if (i == 2) {
                await showModalBottomSheet(
                  shape: OutlineInputBorder(
                      borderSide: BorderSide(color: transparentColor),
                      borderRadius:
                          BorderRadius.vertical(top: Radius.circular(16.0))),
                  context: context,
                  isScrollControlled: true,
                  isDismissible: false,
                  builder: (context) {
                    return Container(
                        height: MediaQuery.of(context).size.width * 1.2,
                        child: LoginNavigator());
                  },
                );
              }
            }
          : null,
      itemCount: widget.videos.length,
    );
  }
}

class VideoPage extends StatefulWidget {
  final String video;
  final String image;
  final int? pageIndex;
  final int? currentPageIndex;
  final bool? isPaused;
  final bool? isFollowing;

  VideoPage(this.video, this.image,
      {this.pageIndex, this.currentPageIndex, this.isPaused, this.isFollowing});

  @override
  _VideoPageState createState() => _VideoPageState();
}

class _VideoPageState extends State<VideoPage> with RouteAware {
  late VideoPlayerController _controller;
  ChewieController? chewieController;
  bool initialized = true;
  bool isLiked = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void didPopNext() {
    print("didPopNext");
    chewieController?.play();
    super.didPopNext();
  }

  @override
  void didPushNext() {
    print("didPushNext");
    chewieController?.pause();
    super.didPushNext();
  }

  @override
  void didChangeDependencies() {
    if (initialized) {
      Future.delayed(Duration.zero).then((value) async {
        _controller = VideoPlayerController.asset(widget.video);
        chewieController = ChewieController(
            videoPlayerController: _controller,
            autoPlay: true,
            looping: true,
            fullScreenByDefault: true);
      });
    }
    initialized = false;
    routeObserver.subscribe(
        this, ModalRoute.of(context) as PageRoute<dynamic>); //Subscribe it here
    super.didChangeDependencies();
  }

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    chewieController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // print(chewieController!.isLive);
    if (widget.pageIndex == widget.currentPageIndex && !widget.isPaused!) {
      if (!initialized) chewieController?.play();
    } else {
      if (!initialized) chewieController?.pause();
    }
    // var locale = AppLocalizations.of(context)!;
//    if (chewieController.value.position == chewieController.value.duration) {
//      setState(() {
//      });
//    }
    if (widget.pageIndex == 2) {
      if (!initialized) chewieController?.pause();
    }
    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: Stack(
        children: <Widget>[
          GestureDetector(
            onTap: () {
              if (!initialized) {
                chewieController!.isPlaying
                    ? chewieController?.pause()
                    : chewieController?.play();
              }
            },
            child: initialized == false
                ? Chewie(controller: chewieController!)
                : SizedBox.shrink(),
          ),
          Positioned.directional(
            textDirection: Directionality.of(context),
            end: -10.0,
            bottom: 80.0,
            child: Column(
              children: <Widget>[
                InkWell(
                  onTap: () {
                    if (!initialized) chewieController?.pause();
                    Navigator.pushNamed(context, PageRoutes.userProfilePage);
                  },
                  child: CircleAvatar(
                      backgroundImage: AssetImage('assets/images/user.webp')),
                ),
                CustomButton(
                  ImageIcon(
                    AssetImage('assets/icons/ic_views.png'),
                    color: secondaryColor,
                  ),
                  '1.2k',
                ),
                CustomButton(
                    ImageIcon(
                      AssetImage('assets/icons/ic_comment.png'),
                      color: secondaryColor,
                    ),
                    '287', onPressed: () {
                  commentSheet(context);
                }),
                CustomButton(
                  Icon(
                    isLiked ? Icons.favorite : Icons.favorite_border,
                    color: secondaryColor,
                  ),
                  '8.2k',
                  onPressed: () {
                    setState(() {
                      isLiked = !isLiked;
                    });
                  },
                ),
                Padding(
                  padding: EdgeInsets.symmetric(vertical: 8.0),
                  child: RotatedImage(widget.image),
                ),
              ],
            ),
          ),
          widget.isFollowing!
              ? Positioned.directional(
                  textDirection: Directionality.of(context),
                  end: 27.0,
                  bottom: 320.0,
                  child: CircleAvatar(
                      backgroundColor: mainColor,
                      radius: 8,
                      child: Icon(
                        Icons.add,
                        color: secondaryColor,
                        size: 12.0,
                      )),
                )
              : SizedBox.shrink(),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
                padding: EdgeInsets.only(bottom: 60.0),
                child: LinearProgressIndicator(
                    //minHeight: 1,
                    )),
          ),
          Positioned.directional(
            textDirection: Directionality.of(context),
            start: 12.0,
            bottom: 72.0,
            child: RichText(
              text: TextSpan(children: [
                TextSpan(
                    text: '@emiliwilliamson\n',
                    style: Theme.of(context).textTheme.bodyText1!.copyWith(
                        fontSize: 16.0,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 0.5)),
                TextSpan(text: 'Comment'),
                TextSpan(
                    text: '  ${'See More'}',
                    style: TextStyle(
                        color: secondaryColor.withOpacity(0.5),
                        fontStyle: FontStyle.italic))
              ]),
            ),
          )
        ],
      ),
    );
  }
}
