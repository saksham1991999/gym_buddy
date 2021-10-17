import 'package:animation_wrappers/animation_wrappers.dart';
import 'package:flutter/material.dart';
import '../Components/entry_field.dart';
import '../../Locale/locale.dart';
import '../Routes/routes.dart';
import '../../Theme/colors.dart';
import '../../Theme/style.dart';

class ChatPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChatBody();
  }
}

class ChatBody extends StatefulWidget {
  @override
  _ChatBodyState createState() => _ChatBodyState();
}

class _ChatBodyState extends State<ChatBody> {
  TextEditingController _messageController = TextEditingController();

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          titleSpacing: 0.0,
          title: ListTile(
            leading: CircleAvatar(
              backgroundImage: AssetImage('assets/user/user2.png'),
            ),
            title: Text(
              'Emili Williamson',
              style: TextStyle(color: secondaryColor),
            ),
            onTap: () =>
                Navigator.pushNamed(context, PageRoutes.userProfilePage),
          ),
        ),
        body: FadedSlideAnimation(
          Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: <Widget>[
              FadedScaleAnimation(MessageStream()),
              Container(
                color: darkColor,
                padding: EdgeInsets.symmetric(horizontal: 12.0),
                child: EntryField(
                  prefix: IconButton(
                    icon: Icon(Icons.tag_faces),
                    color: secondaryColor,
                    onPressed: () {},
                  ),
                  controller: _messageController,
                  hint: 'writeYourComment',
                  suffixIcon: IconButton(
                    icon: Icon(
                      Icons.send,
                      color: mainColor,
                    ),
                    onPressed: () {
                      _messageController.clear();
                    },
                  ),
                  counter: null,
                ),
              ),
            ],
          ),
          beginOffset: Offset(0, 0.3),
          endOffset: Offset(0, 0),
          slideCurve: Curves.linearToEaseOut,
        ));
  }
}

class MessageStream extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // var locale = AppLocalizations.of(context)!;
    final List<MessageBubble> messageBubbles = [
      MessageBubble(
        text: 'Hi rahul',
        time: '01:02 pm',
//      isDelivered: false,
        isMe: true,
      ),
      MessageBubble(
        text: "Rahul looks Amazing!",
        time: '01:02 pm',
//      isDelivered: false,
        isMe: false,
      ),
      MessageBubble(
        text: "Rahul ke dole",
        time: '01:00 pm',
//      isDelivered: false,
        isMe: true,
      ),
      MessageBubble(
        text: "Rahul ke biceps",
        time: '01:00 pm',
//      isDelivered: false,
        isMe: true,
      ),
      MessageBubble(
        text: "Rahul ke family packs!",
        time: '11:59 am',
//      isDelivered: false,
        isMe: false,
      ),
      MessageBubble(
        text: "Rahul ke chubby cheeks!",
        time: '11:58 am',
//      isDelivered: false,
        isMe: false,
      ),
    ];
    return Expanded(
      child: ListView(
        physics: BouncingScrollPhysics(),
        reverse: true,
        padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 20.0),
        children: messageBubbles,
      ),
    );
  }
}

class MessageBubble extends StatelessWidget {
  final bool? isMe;
  final String? text;
  final String? time;
  final bool? isDelivered;

  MessageBubble({this.text, this.time, this.isMe, this.isDelivered});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(10.0),
      child: isMe!
          ? Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: <Widget>[
                Text(
                  time!,
                  style: Theme.of(context).textTheme.caption,
                ),
                SizedBox(width: 12.0),
                Container(
                  constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 2 / 3),
                  decoration: BoxDecoration(
                    color: mainColor,
                    borderRadius: radius,
                  ),
                  padding:
                      EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
                  child: Text(
                    text!,
                    textAlign: TextAlign.end,
                    style: TextStyle(height: 1.4),
                  ),
                ),
              ],
            )
          : Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: <Widget>[
                Container(
                  constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 2 / 3),
                  decoration: BoxDecoration(
                    color: disabledTextColor,
                    borderRadius: radius,
                  ),
                  padding:
                      EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
                  child: Text(
                    text!,
                    style: TextStyle(height: 1.4),
                  ),
                ),
                SizedBox(width: 12.0),
                Text(
                  time!,
                  style: Theme.of(context).textTheme.caption,
                )
              ],
            ),
    );
  }
}
