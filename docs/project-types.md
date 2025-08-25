# Supported Project Types

## 1. simple-service
*Single‐entry binary packaged as a PEX file.*

Directory highlights:
```
services/main/
└── src/.../cli.py        # click-based CLI entry-point
```

---

## 2. api-service
*Stateless REST or gRPC backend.*

Additional components:
* `services/main/src/.../api.py` with **FastAPI** skeleton.
* `Dockerfile` exposes port `8000`.

---

## 3. ml-service
*Adds model training & inference.*

* `models/<model-name>/train.py`  
* `models/<model-name>/inference.py`  
* GPU-ready `Dockerfile.training`.

Retraining can be triggered by pushing data to `data/pipelines/` or via the
scheduled CI workflow.

---

## 4. full-stack
*Backend + React or Next.js front-end.*

* Front-end lives under `apps/web/`.
* Shared **TypeScript types** generated from the OpenAPI spec are placed in
  `packages/api-types/`.

---

## 5. data-pipeline
*Batch processing and feature generation.*

* Airflow DAGs or Spark jobs under `data/pipelines/`.
* Optional ML models consume these features downstream.

---

### Extending a Scaffold

Need a hybrid?  
Generate the closest type and turn on extra features:

```
# Start from api-service, then add ML later
cookiecutter monorepo-template ml_framework=pytorch
```

---

### Decision Flow

1. **Is there a UI?** → choose **full-stack**.  
2. **Serving models?** → starts as **ml-service**.  
3. **No server, just a script?** → **simple-service**.  
4. **Data transforms only?** → **data-pipeline**.  
5. Otherwise → **api-service**.

---

*Last updated: {{ cookiecutter._now.strftime('%Y-%m-%d') }}*
