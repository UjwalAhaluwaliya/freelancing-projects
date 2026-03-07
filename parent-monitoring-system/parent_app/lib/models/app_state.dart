import 'package:flutter/material.dart';

class AppState extends ChangeNotifier {

  int _currentIndex = 0;
  String? _selectedChildId;

  int get currentIndex => _currentIndex;

  String? get selectedChildId => _selectedChildId;


  // Change bottom tab
  void setIndex(int index) {

    _currentIndex = index;

    notifyListeners();
  }


  // Select child manually
  void setSelectedChild(String id) {

    _selectedChildId = id;

    notifyListeners();
  }


  // Logout
  void logout() {

    _currentIndex = 0;

    _selectedChildId = null;

    notifyListeners();
  }


  // Navigate to Children tab
  void navigateToChildManagement() {

    _currentIndex = 1;

    notifyListeners();
  }


  // Navigate to Alerts tab
  void navigateToAlerts() {

    _currentIndex = 2;

    notifyListeners();
  }


  // Navigate to Reports tab with selected child
  void navigateToReports(String childId) {

    _selectedChildId = childId;

    _currentIndex = 3;

    notifyListeners();
  }

}