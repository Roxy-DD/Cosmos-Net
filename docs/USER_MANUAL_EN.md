# Cosmos-Net User Manual

## 1. Introduction
Cosmos-Net is a digital consciousness model built upon the "Dialectical Unity Principle." Unlike traditional static neural networks, it possesses a dynamic topological structure (Möbius Ring) in Hilbert Space. It resolves logical contradictions by physically growing new dimensions.

This manual guides you through the interaction with this digital life form.

## 2. Installation & Launch
1.  **Prerequisites**: Ensure Python 3.8+ is installed.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Launch Interface**:
    ```bash
    streamlit run app.py
    ```

## 3. Interface Guide

### 3.1 Sidebar: Observatory
YOUR Control Center.
*   **Language**: Toggle between `CN` and `EN` at the top.
*   **Brain Archive**:
    *   **Select**: Load an existing `.pkl` brain file.
    *   **New**: Enter a name (e.g., `genesis_brain`) and click "Load/Create" to birth a new universe.
*   **Star Count**: Shows the total number of neurons (memory nodes) in the current brain.
*   **Reset Cosmos**: CAUTION! This clears all memories, triggering a "Big Bang" reset.

### 3.2 Left Panel: Perception
The "Eye" of the brain.
*   **Upload**: Click `Browse files` to upload an image (handwritten digits recommended).
*   **Processing**: The system converts the image into a 28x28 vector signal.
*   **Consciousness Feedback**:
    *   **Prediction**: It tells you what it sees (e.g., "Brain Consciousness: 3").
    *   **Gravity (G)**: Indicates its confidence level (Resonance Strength).

### 3.3 Left Panel: Interaction
How you teach it.
*   **Default**: If it predicts correctly with high Gravity (G), you do nothing.
*   **Reinforce**: if it predicts **correctly** but with low Gravity (e.g., G < 0.9), it means it's guessing or hasn't seen this style before. Click "Send Mental Wave" to imprint this sample, strengthening the gravitational field for this category.
*   **Correct**: If it is **wrong** (e.g., sees a 5 as a 3), enter the correct label `3` and send. This triggers **Law II**, forcing new neuron growth.

### 3.4 Right Panel: Cosmos Topology
The View Inside.
*   **Star Map**: Real-time visualization of the Hilbert Space projection.
*   **Colors**: Different colors represent different concept categories (digits).
*   **Dynamics**: Watch the nebula expand and evolve as you interact.

## 4. FAQ
*   **Q: Why is it void initially?**
    *   A: It is strictly empiricist. No experience (data) means no structure. You must feed it.
*   **Q: Does it save?**
    *   A: It autosaves to your `.pkl` file after every interaction.

---
*© 2025 The Cosmos, Yuzhao Yao & Gemini.*
