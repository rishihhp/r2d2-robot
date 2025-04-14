# 🤖 R2D2: A Real-World AI Agent Powered by Vision & Movement

<img src="https://upload.wikimedia.org/wikipedia/en/3/39/R2-D2_Droid.png" width="150" align="right">

**R2D2** is a fully autonomous, mobile AI robot built with **Raspberry Pi**, **NanoOWL Vision-Language Model (VLM)**, and a dynamic interface. Developed in 36 hours for **TreeHacks @ Stanford**, this droid interacts with the physical world—seeing, thinking, and responding just like a true sci-fi companion.

It’s not just a demo. It’s a glimpse into the future of embodied AI.

---

## 🌟 Features

- 🧠 **NanoOWL-Powered VLM**: Real-time image captioning, understanding, and command recognition.
- 📷 **Vision-Based Perception**: Understands its environment through a Pi Camera and interprets it using a multimodal model.
- 💬 **Natural Interaction**: Talk to R2D2 via typed or spoken commands; it responds with actions or screen feedback.
- 🛞 **Autonomous Mobility**: Moves, turns, and navigates space with motorized wheels and command logic.
- 📺 **On-Screen Personality**: Expresses mood and status via a display screen (yes, it has *attitude*).
- 🔄 **Live Looping AI Agent**: Processes input, responds intelligently, and learns continuously.
- 🌐 **cURL + API Control**: We're adding support for remote HTTP commands to control R2D2’s real-world actions from anywhere.

---

## 🚀 Demo

https://user-images.githubusercontent.com/YOUR-USERNAME/demo-r2d2.mp4

*“Hey R2D2, what’s that object?” → R2D2 turns, identifies a red cup, and says: “That looks like a red Solo cup. Party mode?”*

---

## 🧠 Architecture

```mermaid
graph TD;
    Camera-->NanoOWL;
    Screen<-->RaspberryPi;
    RaspberryPi-->Motors;
    NanoOWL-->DecisionEngine;
    DecisionEngine-->RaspberryPi;
    Mic-->SpeechToText-->NanoOWL;
    WebAPI-->CommandParser-->RaspberryPi;
