# IndustrialPredictAI

Streamlit prototype: simulated equipment monitoring plus an AI4I 2020 failure predictor.

## Project layout

```
app.py
requirements.txt
.streamlit/config.toml
models/failure_prediction_bundle.joblib   <- you must add this
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository and push these files, **including**
   `models/failure_prediction_bundle.joblib` (files under 100 MB are fine;
   do not list `models/` in `.gitignore`).
2. Go to https://share.streamlit.io, sign in with GitHub and click **Create app**.
3. Choose the repository and branch, and set **Main file path** to `app.py`.
4. Under **Advanced settings**, choose Python 3.11 or 3.12.
5. Click **Deploy**. Later `git push` commits redeploy automatically.

## Important: match library versions to your training environment

The `.joblib` bundle is a pickle. Loading it with a different scikit-learn or
XGBoost version can fail or give wrong results. In the environment where you
trained the model, run:

```bash
pip freeze | grep -iE "scikit-learn|xgboost|joblib|numpy|pandas"
```

then pin those exact versions in `requirements.txt` (e.g. `scikit-learn==1.5.2`).
If the model fails to load, the Predictor page shows the error and the rest of
the app keeps working.

## Notes

- Telemetry history lives in each visitor's session and resets when the page reloads.
- Free-tier apps sleep after inactivity; the first visit afterwards wakes them.
