# n8n Resume Shortlist Contract

Event name sent to n8n: `resume_shortlisted`

Top-level payload schema:

```json
{
  "event_version": "1.0",
  "triggered_at": "ISO-8601 UTC timestamp",
  "threshold": 70,
  "hr_user_id": "uuid",
  "candidate": {
    "id": "uuid|null",
    "full_name": "string|null",
    "email": "string|null",
    "phone": "string|null"
  },
  "application": {
    "id": "uuid|null",
    "stage": "string|null",
    "job_id": "uuid|null",
    "candidate_id": "uuid|null"
  },
  "analysis": {
    "match_score": 0,
    "recommendation": "Hire|Consider|Reject",
    "summary": "string",
    "strengths": ["string"],
    "missing_skills": ["string"],
    "raw_output": "string"
  }
}
```

Expected n8n flow:

1. Webhook node receives `event = resume_shortlisted`.
2. Add a `Code` node for JSON validation (hard-fail on malformed payload).
3. Validate `analysis.match_score >= threshold`.
4. Route:
   - Email HR/recruiter with candidate + score summary.
   - Create internal task/notification in workflow target system.
5. Respond with 2xx JSON status to confirm processing.

Recommended n8n Code node snippet:

```javascript
const p = $json?.data;
if (!p) throw new Error("Missing data payload");
if (p.event_version !== "1.0") throw new Error("Invalid event_version");
if (typeof p.threshold !== "number") throw new Error("Invalid threshold");
if (!p.analysis || typeof p.analysis.match_score !== "number") {
  throw new Error("Invalid analysis.match_score");
}
if (p.analysis.match_score < 0 || p.analysis.match_score > 100) {
  throw new Error("match_score out of range");
}
if (!p.hr_user_id) throw new Error("Missing hr_user_id");
return [{ json: p }];
```

Failure behavior:

- FastAPI returns `workflow.ok = false` with error details if n8n call fails.
- FastAPI retries temporary n8n failures (timeouts/429/5xx) with exponential backoff + jitter.
- Resume scoring response still returns to client.
