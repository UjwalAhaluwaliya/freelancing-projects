import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:child_app/main.dart';

void main() {
  testWidgets('App loads smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const ChildControlApp());
    await tester.pumpAndSettle();
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
