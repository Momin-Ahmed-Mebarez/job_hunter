<h1 align="center">(WIP) Job hunter</h1>
<p align="center">Your aid to stay updated with the latest suitable job offers</p>
<p align="center">Local and external LLM support (Only openai compatible)</p>

Installation:
```bash
git clone https://github.com/Momin-Ahmed-Mebarez/job_hunter.git
cd job_hunter
pip install -r requirements.txt
```

Usage:
Please check [Recommendations](Recommendations) before running the script.
```bash
python job_hunter.py
```

Web interface:
Running the script will launch a flask self-hosted server on the provided ip
<p align="center">
  <img src="assets/ip.png" />
</p>
- If conifg.json isn't set then the webpage will redirect you to /config where you can set up LLM usage.
- If you chose to use a LLM you will be directed to /cv to upload your cv.The specified llm will be used to extract rules from your cv. You can create your own cv_rules.txt in /prompts folder (This rules are the prompt used by the LLM to understand it's task)
