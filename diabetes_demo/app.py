import gradio as gr

from src.predict import predict

FEATURE_INFO = [
    ("Pregnancies", "Số lần mang thai", 0, 20, 1, 0),
    ("Glucose", "Nồng độ Glucose (mg/dL)", 0, 200, 1, 120),
    ("BloodPressure", "Huyết áp tâm trương (mm Hg)", 0, 140, 1, 70),
    ("SkinThickness", "Độ dày nếp gấp da (mm)", 0, 100, 1, 20),
    ("Insulin", "Insulin huyết thanh (mu U/ml)", 0, 900, 1, 80),
    ("BMI", "Chỉ số BMI (kg/m²)", 0.0, 70.0, 0.1, 25.0),
    ("DiabetesPedigreeFunction", "Hệ số di truyền tiểu đường", 0.0, 2.5, 0.01, 0.5),
    ("Age", "Tuổi", 1, 120, 1, 30),
]


def classify(*args):
    input_dict = {}
    for i, (col_name, *_) in enumerate(FEATURE_INFO):
        input_dict[col_name] = args[i]

    result = predict(input_dict)

    label = result["label"]
    prob = result["probability_diabetes"] * 100

    output_text = f"### {label}\n\nXác suất mắc tiểu đường: **{prob:.1f}%**"
    return output_text


def create_app():
    inputs = []
    for col_name, label, min_val, max_val, step, default in FEATURE_INFO:
        inputs.append(
            gr.Number(label=label, value=default, minimum=min_val, maximum=max_val)
        )

    app = gr.Interface(
        fn=classify,
        inputs=inputs,
        outputs=gr.Markdown(label="Kết quả dự đoán"),
        title="Dự đoán nguy cơ tiểu đường",
        description="Nhập các chỉ số sức khỏe để dự đoán nguy cơ mắc bệnh tiểu đường.",
        flagging_mode="never",
    )
    return app


if __name__ == "__main__":
    app = create_app()
    app.launch()
