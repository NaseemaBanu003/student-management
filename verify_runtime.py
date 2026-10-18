from app import create_app

app = create_app()
with app.app_context():
    try:
        from app.extensions import db
        db.create_all()
        result = "APP_OK"
    except Exception as exc:  # pragma: no cover
        result = f"APP_FAIL:{type(exc).__name__}:{exc}"

with open(r'd:\smp\verify_runtime.txt', 'w', encoding='utf-8') as fh:
    fh.write(result)
