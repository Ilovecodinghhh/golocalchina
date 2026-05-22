"""
Mission 4: Build the booking API + database migrations.

FLOW: Architect (final endpoint spec) → Builder (implement) → Legal (review code for Path B)
DELIVERABLE: Working FastAPI code + PostgreSQL migrations + project scaffold
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.message_bus import MessageBus, Message, MessageType
from src.agents.architect import ArchitectAgent
from src.agents.builder import BuilderAgent
from src.agents.legal import LegalAgent


def main():
    print("=" * 70)
    print("🎯 MISSION 4: BUILD THE BOOKING API")
    print("=" * 70)
    print()
    print("Deliverables: Project scaffold, DB migrations, core API endpoints")
    print("Flow: Architect → Builder → Legal (code review)")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start = time.time()
    bus = MessageBus()
    architect = ArchitectAgent(bus)
    builder = BuilderAgent(bus)
    legal = LegalAgent(bus)
    results = {}

    # Load context from previous missions
    m2_spec = ""
    if os.path.exists("output/mission-2/DELIVERABLE.md"):
        with open("output/mission-2/DELIVERABLE.md") as f:
            m2_spec = f.read()[:3000]

    m2_legal = ""
    if os.path.exists("output/mission-2/legal_constraints.md"):
        with open("output/mission-2/legal_constraints.md") as f:
            m2_legal = f.read()[:2000]

    log = lambda step, detail="": print(f"\n{'='*70}\n[{time.strftime('%H:%M:%S')}] MISSION 4 — {step}\n  {detail}\n{'='*70}")

    # ================================================================
    # STEP 1: Architect — Produce implementable DB + API spec
    # ================================================================
    log("STEP 1/4", "Architect: Database DDL + API endpoint signatures")

    bus.post(Message(
        sender="mission",
        recipient="architect",
        msg_type=MessageType.REQUEST,
        subject="Produce DDL + API spec for Builder",
        payload=f"""Produce the exact database DDL and API endpoint specifications for the Builder.

PATH B CONSTRAINTS (mandatory):
- No "tour" / "package" / "itinerary" tables or fields
- Use: GuideListing, ServiceRequest, Connection naming
- Guide sets own prices. Platform fee = "信息服务费" (12%)
- Payment flows through licensed PSP (Airwallex), platform never holds funds

TECH STACK (locked from Mission 2):
- Backend: FastAPI (Python) with SQLAlchemy + Alembic
- DB: PostgreSQL 15
- Auth: JWT (access + refresh tokens)
- Cache: Redis

PRODUCE EXACTLY:

1. **Complete DDL** — CREATE TABLE statements for ALL tables:
   - users (with role enum: tourist/guide/admin)
   - tourist_profiles
   - guide_profiles (with 导游证 verification fields)
   - guide_listings (guide-authored, guide-owned)
   - availability_slots
   - service_requests (tourist → guide connection requests)
   - payments (Airwallex references)
   - payouts (guide CNY payouts)
   - reviews (bilateral)
   - messages (with translation fields)
   - consent_records (PIPL compliance)
   - audit_log (immutable)
   Include: primary keys, foreign keys, indexes, constraints, enums.

2. **API endpoints** — For each, give: method, path, request body, response body, auth requirement.
   Priority endpoints for Builder to implement first:
   - POST /api/v1/auth/register
   - POST /api/v1/auth/login
   - GET  /api/v1/guides (search with filters)
   - GET  /api/v1/guides/{{id}}
   - POST /api/v1/guides/{{id}}/service-request
   - GET  /api/v1/service-requests/mine
   - POST /api/v1/reviews

3. **Matching algorithm** — Python pseudocode for guide search ranking.

Keep it concrete. No prose — just DDL, JSON schemas, and code."""
    ))

    responses = architect.receive_and_process()
    db_api_spec = responses[0].payload if responses else "FAILED"
    results["db_api_spec"] = db_api_spec
    print(f"\n📐 Architect produced DB + API spec ({len(db_api_spec):,} chars)")

    # ================================================================
    # STEP 2: Builder — Implement project scaffold + DB + core endpoints
    # ================================================================
    log("STEP 2/4", "Builder: Implement project scaffold, migrations, core API")

    architect.handoff_to(
        "builder",
        "Build: project scaffold + DB migrations + core API endpoints",
        f"""Implement the GoLocalChina backend MVP from the Architect's spec.

ARCHITECT'S SPEC:
{db_api_spec[:5000]}

PRODUCE THE FOLLOWING FILES (output each with its full path and complete content):

1. **Project structure** — List every file and directory

2. **requirements.txt** — All Python dependencies

3. **app/main.py** — FastAPI app factory with CORS, middleware, router mounting

4. **app/core/config.py** — Pydantic Settings for env-based config

5. **app/core/database.py** — SQLAlchemy async engine + session

6. **app/models/base.py** — SQLAlchemy declarative base + mixins

7. **app/models/user.py** — User + TouristProfile + GuideProfile models

8. **app/models/listing.py** — GuideListing + AvailabilitySlot models

9. **app/models/booking.py** — ServiceRequest + Payment + Payout models

10. **alembic/versions/001_initial.py** — Alembic migration with all CREATE TABLE

11. **app/api/v1/auth.py** — Register + Login endpoints (JWT)

12. **app/api/v1/guides.py** — Guide search + detail endpoints with ranking algo

13. **app/api/v1/service_requests.py** — Create service request + list mine

14. **app/schemas/*** — Pydantic v2 request/response schemas

15. **docker-compose.yml** — PostgreSQL + Redis + API

For EACH file, output:
```
### FILE: path/to/file.py
```python
<complete file content>
```

Make it RUNNABLE. Someone should be able to clone this and `docker-compose up`."""
    )

    responses = builder.receive_and_process()
    implementation = responses[0].payload if responses else "FAILED"
    results["implementation"] = implementation
    print(f"\n🔨 Builder produced implementation ({len(implementation):,} chars)")

    # ================================================================
    # STEP 3: Legal — Review code for Path B compliance
    # ================================================================
    log("STEP 3/4", "Legal: Review implementation for Path B red lines")

    builder.handoff_to(
        "legal",
        "Code review: Path B compliance check on implementation",
        f"""Review the Builder's code for Path B compliance violations.

CHECK FOR:
1. Any variable names, table names, endpoint paths, or comments that use 
   "tour", "package", "booking" (should be "service_request", "connection", "listing")
2. Payment flow: does the code imply platform holds funds?
3. Guide relationship: any code that sets guide prices, schedules, or controls their work?
4. Data handling: are consent_records and audit_log tables present?
5. Any hardcoded strings that could be problematic under 广告法?

BUILDER'S CODE:
{implementation[:5000]}

Return: VIOLATIONS FOUND (with file:line and fix) or CLEARED."""
    )

    responses = legal.receive_and_process()
    code_review = responses[0].payload if responses else "FAILED"
    results["code_review"] = code_review
    print(f"\n⚖️  Legal produced code review ({len(code_review):,} chars)")

    # ================================================================
    # STEP 4: Builder — Apply fixes from legal review
    # ================================================================
    log("STEP 4/4", "Builder: Apply legal fixes + produce final file list")

    legal.handoff_to(
        "builder",
        "Apply legal fixes and produce final implementation summary",
        f"""Legal reviewed your code. Apply their fixes and produce a final summary.

LEGAL'S CODE REVIEW:
{code_review[:3000]}

Produce:
1. A numbered list of every change you made (file, what changed, why)
2. The corrected version of any files that had violations
3. A README.md for the project with:
   - Setup instructions (docker-compose up)
   - API documentation (endpoint list with examples)
   - Environment variables needed
   - How to run migrations"""
    )

    responses = builder.receive_and_process()
    final_impl = responses[0].payload if responses else "FAILED"
    results["final_implementation"] = final_impl
    print(f"\n🔨 Builder produced final implementation ({len(final_impl):,} chars)")

    elapsed = time.time() - start

    # Save deliverables
    os.makedirs("output/mission-4", exist_ok=True)

    file_map = {
        "db_api_spec": "01_db_api_spec.md",
        "implementation": "02_implementation.md",
        "code_review": "03_legal_code_review.md",
        "final_implementation": "04_final_implementation.md",
    }
    for key, filename in file_map.items():
        with open(f"output/mission-4/{filename}", "w") as f:
            f.write(results.get(key, "FAILED"))

    with open("output/mission-4/DELIVERABLE.md", "w") as f:
        f.write(f"<!-- Mission 4 | {time.strftime('%Y-%m-%d %H:%M:%S')} | {elapsed:.0f}s | Path B -->\n\n")
        f.write("# GoLocalChina MVP Backend Implementation\n\n")
        f.write(f"## Files Produced\n\n")
        for key, filename in file_map.items():
            size = len(results.get(key, ""))
            f.write(f"- [{filename}](./{filename}) ({size:,} chars)\n")
        f.write(f"\n## Final Implementation\n\n")
        f.write(results.get("final_implementation", "NONE")[:2000])

    with open("output/mission-4/mission_data.json", "w") as f:
        json.dump({
            "mission": "Build booking API + database (Path B)",
            "results": results,
            "messages": [m.to_dict() for m in bus.messages],
            "elapsed_seconds": elapsed,
        }, f, indent=2, default=str)

    # Report
    print(f"\n{'='*70}")
    print(f"📊 MISSION 4 COMPLETE")
    print(f"{'='*70}")
    print(f"  Messages: {len(bus.messages)} | Runtime: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print()
    print("Message flow:")
    for msg in bus.messages:
        icons = {"request": "📨", "response": "📬", "handoff": "🔀"}
        icon = icons.get(msg.msg_type.value, "💬")
        print(f"  {icon} {msg.sender:>12} → {msg.recipient:<12} [{msg.msg_type.value:8}] {msg.subject[:55]}")
    print()
    print("Deliverables:")
    for fn in sorted(os.listdir("output/mission-4")):
        size = os.path.getsize(f"output/mission-4/{fn}")
        print(f"  📄 output/mission-4/{fn} ({size:,} bytes)")
    print(f"\n🏁 Done. Deliverables in output/mission-4/")


if __name__ == "__main__":
    main()
