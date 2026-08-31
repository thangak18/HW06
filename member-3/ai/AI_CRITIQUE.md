# AI Critique (200–300 words)

**Student:** TODO  
**Student ID:** TODO  
**Exercise ID:** HW06-AI  

---

## Critical Reflection on AI Collaboration

*(Place your 200–300 words AI critique paragraph here answering the mandatory assignment prompts):*

1. **Where did the AI get something wrong, biased, or incomplete?**
   - E.g., The AI excelled at generating basic nominal parameter partitions and common negative strings, but frequently overlooked multi-step state mutations and subtle security boundaries (e.g., IDOR on resources belonging to other tenants, race conditions in coupon redemption, or rate-limiting lockout state resets).
2. **Why did it fail to catch the issue?**
   - E.g., The model lacked persistent contextual memory of backend database side-effects and treated individual API calls as stateless functional units rather than nodes in an evolving state machine.
3. **What principle have you learned about collaborating with AI during this assignment?**
   - E.g., AI is an effective accelerator for baseline test scaffolding, but rigorous human auditing, domain-specific state modeling, and strict anti-hallucination verification remain indispensable for high-confidence software quality assurance.
