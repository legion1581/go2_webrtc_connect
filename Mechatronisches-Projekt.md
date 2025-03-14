
# Mechatronisches Projekt: Autonome Fernsteuerung eines Unitree Go2 mit Kollisionsvermeidung

## Projektbeschreibung und Zielsetzung

Das Ziel dieses Projekts ist die Entwicklung einer Fernsteuerungsanwendung für den quadrupedalen Roboter **Unitree Go2**, mit der der Roboter über eine **Tastatur oder einen Game-Controller** navigiert werden kann. Gleichzeitig wird der **Kamerastream** des Roboters in Echtzeit auf einem Monitor angezeigt. 

Die Kernfunktion des Projektes ist, dass der Benutzer sobald der Roboter ferngesteuert wird eine gute Orientierung bekommt, um den Roboter nur auf Basis des Kamerabildes zu steuern. Die Analogie ist die Rückfahrkameras von Autos, die eine visuelle Rückmeldung bekommen, um sich besser zu orientieren. 

Eine Kernfunktion des Projekts ist die **Kollisionsvermeidung/warnung** basierend auf den **Lidar-Daten**, um sicherzustellen, dass der Roboter einen definierten Sicherheitsabstand zu Hindernissen nicht unterschreitet. 

Zusätzlich soll der Roboter seine eigene **Geometrie ins Kamerabild projizieren**, um dem Bediener visuelles Feedback über die Passierbarkeit enger Durchgänge zu geben.

>:rocket: Das Projekt soll den Studenten eine praxisnahe Einführung in die Themen **Robotik, Sensordatenverarbeitung und Computer-Vision** geben und gleichzeitig Fähigkeiten in **Softwareentwicklung** und **mechatronischer Systemintegration** fördern.

![](Go2-Air.png)

## Verwendete Hardware
- **Unitree Go2** - Quadrupedaler Roboter
  - **LiDAR-Scanner** für Umgebungswahrnehmung
  - **RGB-Kamera** zur Live-Übertragung des Videostreams
- **Game-Controller oder Tastatur** für die Fernsteuerung
- **NVidia Jetson AGX 64GB**  Entwicklungsplattform (alternativ eigener Laptop)
- Alternative Hardware: Intelrealsense Tiefenkamera statt Lidar

## Verwendete Software
- **WebRTC** 
- **Python** 
- **REST API / FastRTC** 
- **OpenCV**
- **Docker**
- **Linux (Ubuntu)**

## Aufgabenpakete
0. **Entscheidung über das Hardware Setup:**
   - Verwendung der RGB Kamera + Lidar (a) oder Verwenden der IntelRealsense RGB-D Kamera (b)
   - Definition der Features und Funktionen, die entweickelt werden sollen (Archtecture Inseption Canvas)
   - Definition der Test-Szenarien
   - Identifikation externer Arbeitspakete
   - Im Fall von b: Konstruktion des Aufbaus auf dem Roboterhund

2. **Einrichtung der Fernsteuerung**
   - Implementierung der Steuerung über Tastatur und Game-Controller
   - Übersetzung der Eingaben in Bewegungsbefehle für den Roboter

3. **Kamerakalibrierung**
   - Aufnahme von Kalibrierbildern mit Schachbrettmuster oder Charuco-Board
   - Bestimmung der Kameramatrix und Verzerrungsparameter mit OpenCV
   - Anwendung der Kalibrierung auf den Live-Videostream zur Korrektur von Verzerrungen
   
4. **Live-Kamerastream mit WebRTC (Robotercom) und fastRTC (Streaming)**
   - Zugriff auf den RGB-Kamerastream
   - Echtzeitübertragung des Videostreams an einen Monitor
   
5. **Kollisionsvermeidung/warnung mit LiDAR**
   - Verarbeitung der Laserscanner-Daten
   - Definition eines Sicherheitsabstands und Notfallstopps
   - Visuelle oder andere Warnungen bei zu nahen Hindernissen
   
6. **Geometrieprojektion in das Kamerabild**
   - Berechnung der Robotergeometrie und Anzeige im Livebild
   - Projektion von zwei aufeinander zulaufenden Linien, die die Breite des Roboters symbolisieren
  
7. **Integration und Tests**
   - Zusammenspiel aller Module testen und debuggen
   - Durchführung von Experimenten in realen Szenarien
   - Schriftliche Dokumentaiton des Projektes

## Vorkenntnisse

- Softwareentwicklung
- Optional: Computer Vision
- Optional: Konstruktion und 3D-Druck

## Literatur:  

Kamera: 
- What is lens distortion and camera calibration? 
  - [https://de.mathworks.com/help/vision/ug/camera-calibration.html](https://de.mathworks.com/help/vision/ug/camera-calibration.html)
  - [https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)
  - [https://wiki.ros.org/camera_calibration](https://wiki.ros.org/camera_calibration)
- How to undistort the camera image: 
  - from section "Undistortion": [https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)

Technologien:
- https://github.com/freddyaboulton/fastrtc
- https://fastapi.tiangolo.com

Go2:
- https://github.com/legion1581/go2_webrtc_connect
- https://github.com/abizovnuralem/go2_ros2_sdk/tree/chore/update-docker-to-ros-humble

Vorlesung: 
- MTB: ITEC - Software Engineering
- DEB: Technische Informatik
