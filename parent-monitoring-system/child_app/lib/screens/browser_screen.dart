import 'dart:async';
import 'package:flutter/material.dart';
import 'package:child_app/services/api_service.dart';
import 'package:child_app/services/child_service.dart';
import 'package:webview_flutter_android/webview_flutter_android.dart';
import 'package:webview_flutter/webview_flutter.dart';

class BrowserScreen extends StatefulWidget {

  const BrowserScreen({
    super.key,
    required this.onBlocked,
  });

  final VoidCallback onBlocked;

  @override
  State<BrowserScreen> createState() => _BrowserScreenState();
}

class _BrowserScreenState extends State<BrowserScreen>{

  final TextEditingController _urlController =
      TextEditingController(text: "youtube.com");

  late WebViewController _webController;

  Timer? _timer;

  bool _blocked = false;
  bool _checking = false;

  @override
  void initState() {

    super.initState();

    _webController = WebViewController()

      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setUserAgent(
        "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
      )

      ..setNavigationDelegate(

        NavigationDelegate(
          onNavigationRequest: (request) => NavigationDecision.navigate,

          onPageFinished: (url) {

            _startUsageTimer();

          },

        ),

      );

    if (_webController.platform is AndroidWebViewController) {
      final androidController = _webController.platform as AndroidWebViewController;
      androidController.setMediaPlaybackRequiresUserGesture(false);
    }
  }


  /// Usage tracking every 1 minute
 /// Usage tracking every 1 minute with Active Blocking
  void _startUsageTimer() {
    if (_timer != null) return;

    _timer = Timer.periodic(
      const Duration(minutes: 1),
      (t) async {
        final today = DateTime.now().toIso8601String().split('T')[0];

        try {
          final response = await ApiService.instance.post(
            "/child/log-usage",
            body: {
              "usage_time": 1,
              "date": today
            }
          );

          // ACTIVE BLOCKING LOGIC
          if (response['limit_exceeded'] == true) {
            _timer?.cancel(); // Stop the timer
            setState(() {
              _blocked = true; // Show the Red Blocked Screen
            });
            widget.onBlocked(); // Notify parent logic if needed
          }
        } catch (e) {
          debugPrint("Usage Log Failed: $e");
        }
      }
    );
  }


  Future<void> openUrl() async {

    String url = _urlController.text.trim();

    if(url.isEmpty){

      ScaffoldMessenger.of(context).showSnackBar(

        const SnackBar(
            content:Text("Enter URL")
        )

      );

      return;

    }

    if(!url.startsWith("http")){

      url="https://$url";

    }

    setState(()=>_checking=true);

    try{

      final urlCheck = await ChildService.instance.checkUrl(_urlController.text);

      if(!urlCheck.allowed){

        if (urlCheck.reason == "time_limit") {
          setState(() {
            _checking = false;
          });
          widget.onBlocked();
          return;
        }

        setState((){

          _blocked=true;
          _checking=false;

        });

        return;

      }

      setState(()=>_checking=false);

      _webController.loadRequest(
          Uri.parse(url)
      );

    }
    catch(e){

      setState(()=>_checking=false);
      if (!mounted) return;

      ScaffoldMessenger.of(context)
          .showSnackBar(

        const SnackBar(
            content:Text("Connection Error")
        ),

      );

    }

  }


  void _resetBlocked(){

    setState(()=>_blocked=false);

  }


  @override
  void dispose(){

    _timer?.cancel();

    _urlController.dispose();

    super.dispose();

  }


  @override
  Widget build(BuildContext context){

    /// BLOCKED SCREEN
    if(_blocked){

      return Scaffold(

        appBar:AppBar(
            title:const Text("Browser")
        ),

        body:Center(

          child:Column(

            mainAxisAlignment:
            MainAxisAlignment.center,

            children:[

              Icon(
                Icons.block,
                size:80,
                color:Colors.red,
              ),

              const SizedBox(height:20),

              const Text(
                "Access Blocked",
                style:TextStyle(
                    fontSize:22,
                    fontWeight:FontWeight.bold
                ),
              ),

              const SizedBox(height:10),

              const Text(
                  "Restricted by Parent"
              ),

              const SizedBox(height:20),

              ElevatedButton(

                onPressed:_resetBlocked,

                child:const Text(
                    "Try Another URL"
                ),

              )

            ],

          ),

        ),

      );
    }


    /// BROWSER SCREEN
    return Scaffold(

      appBar:AppBar(

        title:const Text("Browser"),

      ),

      body:Column(

        children:[

          Padding(

            padding:
            const EdgeInsets.all(10),

            child:Row(

              children:[

                Expanded(

                  child:TextField(

                    controller:_urlController,

                    decoration:

                    InputDecoration(

                      hintText:"youtube.com",

                      border:
                      OutlineInputBorder(),

                    ),

                    onSubmitted:(_)=>openUrl(),

                  ),

                ),

                const SizedBox(width:8),

                _checking
                    ? const CircularProgressIndicator()
                    : IconButton(

                    onPressed:openUrl,

                    icon:const Icon(
                        Icons.open_in_browser
                    )

                )

              ],

            ),

          ),

          Expanded(

            child:WebViewWidget(
                controller:_webController
            ),

          )

        ],

      ),

    );

  }

}
