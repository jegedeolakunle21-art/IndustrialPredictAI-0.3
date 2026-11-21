# IndustrialPredictAI v0.3
### An Industrial Equipment Monitoring and Machine Learning Prototype

**IndustrialPredictAI** is a project I developed to explore how machine learning and data-driven monitoring can support equipment reliability and predictive maintenance in industrial environments.

The idea behind this project is straightforward: equipment such as motors, pumps and generators produces operating information that can help engineers understand equipment behaviour, identify unusual conditions and make better maintenance decisions.

I wanted to bring some of these ideas together in a practical application by combining a simulated equipment monitoring dashboard with a machine learning-based failure prediction tool.

The current version is a working prototype, built with Python and Streamlit.

## What does the application do?

IndustrialPredictAI currently has two main functional components.

### 1. Live Equipment Monitoring

This section provides a simulated monitoring environment for selected industrial equipment, including:

- Electric motors
- Pumps
- Generators

The dashboard generates simulated operating readings for:

- Temperature (°C)
- Vibration (mm/s)
- Electrical current
- Pressure

Readings refresh automatically every five seconds, allowing users to observe changes in equipment operating conditions.

The application also calculates illustrative equipment health scores and assigns three operating categories:

- Healthy
- Warning
- Critical

Users can explore telemetry trends and view alerts when simulated operating conditions fall outside the application's predefined thresholds.

**An important distinction:** The monitoring section currently uses simulated sensor readings. It is intended to demonstrate how an industrial monitoring dashboard could work, rather than represent measurements from actual industrial equipment.

### 2. AI4I Machine Failure Predictor

The second component explores the application of machine learning to manufacturing equipment failure prediction.

It uses a trained machine learning pipeline developed with the AI4I 2020 Predictive Maintenance dataset.

Users can enter operating parameters, including:

- Product type
- Air temperature
- Process temperature
- Rotational speed
- Torque
- Tool wear

The model processes these inputs and produces an estimated failure probability.

The application then compares the probability against a configurable decision threshold to classify the input as either a potential machine failure or no predicted failure.

The model's evaluation information is also available within the application.

This section demonstrates how machine learning can be incorporated into an engineering workflow to support condition assessment and predictive maintenance research.

It is important to note that the AI4I benchmark model has not been validated for direct application to the motors, pumps or generators displayed in the simulated monitoring dashboard.

## Why I developed this project

Equipment downtime can affect productivity, operating costs and equipment availability. In many industrial environments, maintenance decisions still depend heavily on scheduled inspections and responses to equipment breakdowns.

Machine learning offers opportunities to complement these traditional approaches through data analysis, pattern recognition and predictive modelling.

I developed IndustrialPredictAI to gain practical experience in connecting engineering concepts with machine learning and interactive software development.

The project also provides a foundation for exploring how simulated sensor data, equipment monitoring and predictive models could eventually be integrated into a more comprehensive industrial intelligence platform.

## Technology Stack

The application was developed using the following technologies:

| Technology | Application |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard and application interface |
| Pandas | Data processing and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning pipeline |
| XGBoost | Machine learning model support |
| Joblib | Model serialization and loading |
| Plotly | Interactive data visualisation |
| SHAP | Explainable AI development support |

## Project Structure

```text
IndustrialPredictAI-0.3/
│
├── streamlit_app.py
│
├── failure_prediction_bundle.joblib
│
├── requirements.txt
│
├── LICENSE
│
└── README.md
```

The model bundle contains the trained prediction pipeline and associated model information required by the application.

## Running the Application Locally

You can run the application on your computer by following these steps.

**Step 1: Clone the repository**

```bash
git clone https://github.com/jegedeolakunle21-art/IndustrialPredictAI-0.3.git
```

**Step 2: Enter the project directory**

```bash
cd IndustrialPredictAI-0.3
```

**Step 3: Create a virtual environment**

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux or macOS:

```bash
source venv/bin/activate
```

**Step 4: Install the dependencies**

```bash
pip install -r requirements.txt
```

**Step 5: Start the application**

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local address where you can access the dashboard through your browser.

## Data and Model Considerations

The project currently combines two different data approaches.

**Simulated telemetry:** The live equipment monitor generates artificial sensor readings for demonstration purposes. These readings are not collected from physical equipment.

**AI4I 2020 benchmark data:** The machine failure predictor uses a trained model based on the AI4I 2020 Predictive Maintenance dataset. The benchmark data are not operational records from the equipment displayed in the monitoring dashboard.

This distinction matters because a machine learning model can achieve good evaluation results on its development dataset without necessarily performing equally well under different real-world operating conditions.

For that reason, IndustrialPredictAI should be viewed as an engineering and machine learning prototype, not a fully validated industrial predictive maintenance solution.

## Current Development Roadmap

IndustrialPredictAI is an ongoing development project. Some of the areas I intend to explore in future versions include:

1. **Real-time IoT integration:** Connecting actual industrial sensors and equipment data sources to the monitoring dashboard.

2. **Equipment-specific machine learning:** Developing and evaluating separate prediction models for motors, pumps and generators using relevant equipment data.

3. **Advanced anomaly detection:** Exploring unsupervised learning techniques to identify unusual operating patterns.

4. **Explainable AI:** Improving the interpretation of machine learning predictions using SHAP and other model explanation techniques.

5. **Historical data management:** Introducing persistent storage to support equipment history, trend analysis and maintenance reporting.

6. **Industrial digital transformation:** Exploring the integration of machine learning, condition monitoring and industrial data infrastructure into a more connected maintenance environment.

## Project Status

**Version:** 0.3

**Development stage:** Working prototype

**Application framework:** Streamlit

**Data approach:** Simulated telemetry and AI4I 2020 benchmark dataset

**Deployment:** Streamlit-compatible application

## Important Disclaimer

IndustrialPredictAI is an independent engineering and machine learning development project.

It is intended for educational, research and demonstration purposes. Its simulated health scores and alerts are illustrative indicators, not validated engineering diagnoses or failure probabilities.

The machine learning predictor is based on a benchmark dataset and has not been validated for real-world industrial equipment deployment.

It should not be used as a substitute for professional equipment inspections, established maintenance procedures, safety systems or engineering judgement.

## About the Developer

I am a Mechanical Engineer with interests in thermofluids, energy systems, machine learning, computational fluid dynamics and industrial digital transformation.

My work focuses on exploring how engineering knowledge, data analytics and artificial intelligence can be combined to address practical engineering challenges.

IndustrialPredictAI is part of my ongoing effort to develop practical, open-source engineering applications that connect traditional engineering disciplines with emerging digital technologies.

I welcome feedback, technical discussions and opportunities for collaboration.

**Author:** Olakunle Jegede

**GitHub:** [github.com/jegedeolakunle21-art](https://github.com/jegedeolakunle21-art)

---

*Building practical engineering solutions through the integration of mechanical engineering, machine learning and industrial digital transformation.*
