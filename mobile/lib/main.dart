import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const NekrosApp());

const red = Color(0xFFFF2638);
const dark = Color(0xFF09090D);

class NekrosApp extends StatelessWidget {
  const NekrosApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'NEKROS',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: dark,
        colorScheme: ColorScheme.fromSeed(seedColor: red, brightness: Brightness.dark),
        useMaterial3: true,
      ),
      home: const AssistantPage(),
    );
  }
}

class Message {
  final String text;
  final bool user;
  const Message(this.text, this.user);
}

class AssistantPage extends StatefulWidget {
  const AssistantPage({super.key});

  @override
  State<AssistantPage> createState() => _AssistantPageState();
}

class _AssistantPageState extends State<AssistantPage> {
  final controller = TextEditingController();
  final scrollController = ScrollController();
  final messages = <Message>[
    const Message('سلام. من NEKROS هستم. هسته اندرویدی من آماده اتصال به سرور هوش مصنوعی است.', false),
  ];
  bool sending = false;
  final apiController = TextEditingController();

  Future<void> send() async {
    final text = controller.text.trim();
    if (text.isEmpty || sending) return;
    setState(() {
      messages.add(Message(text, true));
      sending = true;
    });
    controller.clear();
    try {
      final base = apiController.text.trim().replaceAll(RegExp(r'/+$'), '');
      if (base.isEmpty) {
        setState(() => messages.add(const Message(
          'پیامت دریافت شد؛ اما هنوز آدرس سرور NEKROS تنظیم نشده است. از منوی تنظیمات، آدرس سرور و توکن API را وارد کن.',
          false,
        )));
      } else {
        final response = await http.post(
          Uri.parse('$base/api/chat'),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ${tokenController.text.trim()}',
          },
          body: jsonEncode({'content': text}),
        ).timeout(const Duration(seconds: 30));
        if (response.statusCode >= 200 && response.statusCode < 300) {
          final data = jsonDecode(response.body) as Map<String, dynamic>;
          setState(() => messages.add(Message(data['reply']?.toString() ?? 'پاسخی دریافت نشد.', false)));
        } else {
          setState(() => messages.add(Message('خطای سرور: HTTP ${response.statusCode}', false)));
        }
      }
    } catch (e) {
      setState(() => messages.add(Message('ارتباط با سرور برقرار نشد: $e', false)));
    } finally {
      setState(() => sending = false);
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (scrollController.hasClients) {
          scrollController.animateTo(scrollController.position.maxScrollExtent,
              duration: const Duration(milliseconds: 250), curve: Curves.easeOut);
        }
      });
    }
  }

  final tokenController = TextEditingController();

  void openSettings() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF17171E),
      builder: (context) => Padding(
        padding: EdgeInsets.fromLTRB(20, 20, 20, MediaQuery.of(context).viewInsets.bottom + 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('اتصال به هسته NEKROS', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            TextField(controller: apiController, decoration: const InputDecoration(labelText: 'آدرس سرور، مانند https://example.com')),
            const SizedBox(height: 8),
            TextField(controller: tokenController, obscureText: true, decoration: const InputDecoration(labelText: 'توکن API')),
            const SizedBox(height: 16),
            SizedBox(width: double.infinity, child: FilledButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('ذخیره موقت'),
            )),
            const Text('این نسخه فعلاً تنظیمات را فقط تا زمان بسته‌شدن برنامه نگه می‌دارد.', style: TextStyle(color: Colors.white54, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    controller.dispose();
    apiController.dispose();
    tokenController.dispose();
    scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: const Color(0xFF111116),
          title: const Row(children: [
            Icon(Icons.blur_on, color: red, size: 30),
            SizedBox(width: 8),
            Text('NEKROS', style: TextStyle(letterSpacing: 2, fontWeight: FontWeight.w800)),
          ]),
          actions: [IconButton(onPressed: openSettings, icon: const Icon(Icons.settings_outlined))],
        ),
        body: Column(children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 22),
            decoration: const BoxDecoration(
              gradient: RadialGradient(colors: [Color(0x553D0710), dark], radius: 1.3),
            ),
            child: Column(children: [
              Container(
                width: 112, height: 112,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: red.withOpacity(.8), width: 2),
                  boxShadow: [BoxShadow(color: red.withOpacity(.25), blurRadius: 28, spreadRadius: 5)],
                ),
                child: const Icon(Icons.all_inclusive, color: red, size: 72),
              ),
              const SizedBox(height: 10),
              const Text('NEKROS CORE', style: TextStyle(color: red, letterSpacing: 3, fontWeight: FontWeight.bold)),
              const Text('هسته اندرویدی • نسخه آزمایشی', style: TextStyle(color: Colors.white54, fontSize: 12)),
            ]),
          ),
          Expanded(child: ListView.builder(
            controller: scrollController,
            padding: const EdgeInsets.all(14),
            itemCount: messages.length,
            itemBuilder: (context, index) {
              final m = messages[index];
              return Align(
                alignment: m.user ? Alignment.centerRight : Alignment.centerLeft,
                child: Container(
                  constraints: const BoxConstraints(maxWidth: 310),
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.all(13),
                  decoration: BoxDecoration(
                    color: m.user ? const Color(0xFF351018) : const Color(0xFF191920),
                    border: Border.all(color: m.user ? red.withOpacity(.45) : Colors.white12),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(m.text, style: const TextStyle(height: 1.5)),
                ),
              );
            },
          )),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 6, 12, 12),
              child: Row(children: [
                Expanded(child: TextField(
                  controller: controller,
                  minLines: 1, maxLines: 4,
                  onSubmitted: (_) => send(),
                  decoration: InputDecoration(
                    hintText: 'با NEKROS صحبت کن...',
                    filled: true, fillColor: const Color(0xFF191920),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
                  ),
                )),
                const SizedBox(width: 8),
                IconButton.filled(
                  style: IconButton.styleFrom(backgroundColor: red, foregroundColor: Colors.white),
                  onPressed: sending ? null : send,
                  icon: sending
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    : const Icon(Icons.arrow_upward),
                ),
              ]),
            ),
          ),
        ]),
      ),
    );
  }
}
