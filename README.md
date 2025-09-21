# Fish-Species-Predictor-App

``` mermaid


graph TD
    A[Start] --> B{Launch app.py};
    B --> C{Load Model};
    C --> D{Model Loaded?};
    D -- No --> E[Display Error Message];
    D -- Yes --> F[Display UI with Sidebar Inputs];
    F --> G{User Enters Fish Measurements};
    G --> H{User Clicks 'Predict' Button};
    H --> I[Create DataFrame from Inputs];
    I --> J[Model Makes Prediction];
    J --> K[Display Predicted Weight];
    K --> F;
    E --> L[End];
    K --> L;

```
