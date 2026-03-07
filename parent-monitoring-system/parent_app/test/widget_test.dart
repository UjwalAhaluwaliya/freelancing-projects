import 'package:flutter_test/flutter_test.dart';

import 'package:parent_app/main.dart';

void main() {
  testWidgets('app boots', (WidgetTester tester) async {
    await tester.pumpWidget(const ParentControlApp());
    expect(find.byType(ParentControlApp), findsOneWidget);
  });
}
