## DisasterVision AI

**DisasterVision AI** is an AI-based disaster assessment and decision-support system designed to improve situation awareness during emergency response. The system uses **DeepLabV3 with a ResNet-50 backbone** to perform semantic segmentation on post-disaster UAV imagery, identifying important features such as damaged buildings, roads, water, vegetation, and other disaster-related areas.

The system integrates **Grad-CAM Explainable AI (XAI)** to provide visual explanations of model predictions. It also analyses disaster scenes, assesses severity, generates operational recommendations, and presents the results through an interactive **Streamlit dashboard** with automated situation-report generation.

### Key Features

* UAV disaster image analysis
* DeepLabV3 semantic segmentation
* ResNet-50 feature extraction
* Grad-CAM explainability
* Disaster severity assessment
* AI-generated operational recommendations
* Interactive Streamlit dashboard
* Automated disaster situation reports

Project structure
DVAI\
 -checkpoints
 -modules
 -temp
 -ui
 -app
 -requirements


The dataset for this project is public licenced and can be downloaded here  - https://www.kaggle.com/datasets/yaroslavchyrko/rescuenet

The best checkpoint for this model was excluded from the commit due to Github LFS issues, but can be accessed here via this link -
 - https://drive.google.com/file/d/1s_o2SawvXjkl1GyMeeDe9rO_uSXZirTl/view?usp=drive_link

 - The checkpoint file should be put in the checkpoint folder.


   To run the app, Run
   Streamlit run app.py  in the terminal
   
