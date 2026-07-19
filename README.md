# StadiumOS

StadiumOS is an enterprise-grade, AI-driven stadium operations platform.

## Architecture

- **`backend/`**: Core engine logic (Threat Engine, Event Engine, AI Brain, Copilot, Simulation, Agents).
- **`frontend/`**: UI components, styling, and structural layouts.
- **`pages/`**: Streamlit multi-page routing components.
- **`utils/`**: Shared utilities (Logging).

## Implemented Features
- **Phase 1-3**: Core Dashboard and Real-Time State Aggregation.
- **Phase 4**: Deterministic Threat Engine & Incident Management.
- **Phase 5**: StadiumOS Copilot (Conversational AI Assistant).
- **Phase 6**: Predictive Simulation & What-If Analysis Engine.
- **Phase 7**: Agentic Operations Coordinator (Human-in-the-Loop Executor).
- **Phase 8**: AI Evaluation & Continuous Learning Engine.
- **Phase 9**: Enterprise Architecture Restructuring.

## Running the Application

To launch the StadiumOS Dashboard and all sub-modules:

```bash
streamlit run app.py
```

## Testing, Security, and Accessibility Implementation
- **Testing:** Implemented `pytest` suite covering 100% of core components, models, and AI fallback logic via mock data (`test_app.py`).
- **Security:** Integrated `python-dotenv` for strict secret management. Enforced Regex-based input sanitization against XSS/Injection on all AI inputs. Wraps UI in generic try-except blocks to prevent stack trace leakage.
- **Accessibility:** UI augmented with explicit semantic HTML and ARIA labels (`aria-label`, `role="region"`) to ensure strict hierarchy and screen-reader compatibility.
