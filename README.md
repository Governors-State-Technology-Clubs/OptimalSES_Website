# OptimalSES_Website

Website for Optimal SES, a construction company, built by the GSU Software Engineering Club using HTML, CSS, Flask. on render.
Contributers are as followed:







### VS Code GUI: Commit & Push
1. Left sidebar → **Source Control** (branch icon).
2. Type a clear message (e.g., `feat(about): add hero + intro`).
3. Click **✔ Commit**.
4. Click the **cloud ↑** (Push/Sync). If asked to **Publish branch**, click **Yes**.

---

### Open a Pull Request (PR)
- After you push, GitHub shows **Compare & pull request** → click it.
- Fill out the PR template and attach **desktop + mobile** screenshots.
- Branch protection requires **1 approval** before merge.



### Common Fixes
- **Push to main rejected:** create a feature branch and push that.
- **Permission denied:** ask a lead to add you as a collaborator (Write) or use fork → PR.
- **Out of date with main:**
  ```bash
  git checkout main
  git pull
  git checkout <your-branch>
  git merge main
