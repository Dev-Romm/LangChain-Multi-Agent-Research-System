import re

import streamlit as st


st.set_page_config(
	page_title="Fieldnote | Research System",
	page_icon="F",
	layout="wide",
	initial_sidebar_state="expanded",
)


st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
	:root { --ink:#eef3ef; --muted:#9aa9a6; --line:#344541; --paper:#111a1c; --white:#192527; --teal:#53c2b0; --teal-soft:#1d403d; --coral:#f08a6d; }
	html, body, [class*="css"] { font-family:'Manrope',sans-serif; color:var(--ink); }
	.stApp { background:var(--paper); } [data-testid="stHeader"] { background:rgba(17,26,28,.88); }
	[data-testid="stSidebar"] { background:#172426; border-right:1px solid var(--line); }
	[data-testid="stSidebar"] > div:first-child { padding:2rem 1.35rem; }
	.block-container { max-width:1260px; padding:3.2rem 3.5rem 4rem; }
	h1, h2, h3 { letter-spacing:0; color:var(--ink); } h1 { font-size:clamp(2.2rem,4vw,4.6rem); line-height:.98; margin:0; font-weight:800; }
	h2 { font-size:1.35rem; margin-top:.2rem; } p { color:var(--muted); }
	.eyebrow, .mono { font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.08em; }
	.eyebrow { color:var(--teal); font-size:.72rem; font-weight:500; margin-bottom:.9rem; }
	.hero-copy { max-width:640px; font-size:1.05rem; line-height:1.7; margin:1.2rem 0 0; }
	.rule { height:1px; background:var(--line); margin:2.7rem 0 2rem; }
	.metric { border-top:2px solid var(--teal); padding-top:.8rem; } .metric-number { font-size:1.75rem; font-weight:800; }
	.metric-label { color:var(--muted); font-size:.78rem; } .section-kicker { color:var(--coral); font-size:.7rem; margin-bottom:.6rem; }
	.result-card { background:var(--white); border:1px solid var(--line); padding:1.35rem 1.5rem; margin-bottom:1rem; }
	.result-card h3 { margin:0 0 .55rem; font-size:1rem; } .result-card p { margin:0; line-height:1.65; font-size:.9rem; }
	.source-link { color:var(--teal); font-size:.86rem; overflow-wrap:anywhere; }
	.status-chip { display:inline-block; background:var(--teal-soft); color:var(--teal); padding:.3rem .6rem; font:500 .7rem 'DM Mono',monospace; text-transform:uppercase; }
	.empty-state { border:1px dashed #4b625d; padding:3rem 2rem; text-align:center; background:rgba(25,37,39,.55); }
	.empty-state strong { display:block; font-size:1.1rem; margin-bottom:.4rem; }
	div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input { background:var(--white); border:1px solid #49615c; border-radius:2px; color:var(--ink); }
	.stButton > button { border-radius:2px; font-weight:700; min-height:2.8rem; color:#000 !important; } .stButton > button[kind="primary"] { background:var(--teal); border-color:var(--teal); color:#000 !important; }
	.stDownloadButton > button { border-radius:2px; width:100%; color:#000 !important; } [data-testid="stMetric"] { background:transparent; border:0; padding:0; }
	</style>
	""",
	unsafe_allow_html=True,
)


def extract_sources(search_results: str) -> list[str]:
	urls = re.findall(r"https?://[^\s)]+", search_results or "")
	return list(dict.fromkeys(url.rstrip(".,") for url in urls))


def render_sidebar() -> None:
	with st.sidebar:
		st.markdown("<div class='eyebrow'>FIELDNOTE / 01</div>", unsafe_allow_html=True)
		st.markdown("## Research System")
		st.caption("A four-stage workspace for turning live web research into a considered report.")
		st.markdown("---")
		st.markdown("**Pipeline**")
		for number, label in [("01", "Search the web"), ("02", "Read a primary source"), ("03", "Draft the report"), ("04", "Critique the result")]:
			st.markdown(f"`{number}`  {label}")
		st.markdown("---")
		st.markdown("**Connection status**")
		st.markdown("<span class='status-chip'>Ready to research</span>", unsafe_allow_html=True)
		st.caption("Requires TAVILY_API_KEY and Azure OpenAI environment variables.")


def render_results(state: dict, topic: str) -> None:
	sources = extract_sources(state.get("search_results", ""))
	st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
	st.markdown("<div class='section-kicker mono'>RESEARCH OUTPUT</div>", unsafe_allow_html=True)
	st.header("Your research brief")
	st.caption(topic)
	metric_columns = st.columns(3)
	with metric_columns[0]:
		st.markdown(f"<div class='metric'><div class='metric-number'>{len(sources) or '—'}</div><div class='metric-label'>sources identified</div></div>", unsafe_allow_html=True)
	with metric_columns[1]:
		st.markdown(f"<div class='metric'><div class='metric-number'>{len(state.get('scraped_content', '')):,}</div><div class='metric-label'>characters read</div></div>", unsafe_allow_html=True)
	with metric_columns[2]:
		st.markdown("<div class='metric'><div class='metric-number'>4 / 4</div><div class='metric-label'>stages completed</div></div>", unsafe_allow_html=True)
	report_tab, sources_tab = st.tabs(["Report", "Sources"])
	with report_tab:
		st.markdown(state.get("report", "No report was returned."))
		st.download_button("Download report", data=state.get("report", ""), file_name="research-report.md", mime="text/markdown")
	with sources_tab:
		if sources:
			for source in sources:
				st.markdown(f"<div class='result-card'><a class='source-link' href='{source}' target='_blank'>{source}</a></div>", unsafe_allow_html=True)
		else:
			st.info("No URLs were detected in the search response.")
		with st.expander("View raw search notes"):
			st.text(state.get("search_results", ""))
	with st.expander("View scraped source content"):
		st.text(state.get("scraped_content", ""))

	st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
	st.markdown("<div class='section-kicker mono'>QUALITY REVIEW</div>", unsafe_allow_html=True)
	st.header("Critic report")
	st.caption("An independent pass over the report's evidence, structure, and clarity.")
	st.markdown(f"<div class='result-card'>{state.get('feedback', 'No critique was returned.')}</div>", unsafe_allow_html=True)

	st.markdown("<div class='section-kicker mono'>SESSION TRACE</div>", unsafe_allow_html=True)
	with st.expander("How this brief was produced", expanded=True):
		trace = [
			("01 / Search", "The search agent queried Tavily for recent, reliable sources related to your question."),
			("02 / Read", "The reader agent selected a relevant URL and extracted its main content for deeper context."),
			("03 / Write", "The writer combined the search notes and scraped content into a structured research report."),
			("04 / Critique", "The critic evaluated the completed report and returned a score, strengths, and improvements."),
		]
		for label, detail in trace:
			st.markdown(f"**{label}**  \n{detail}")


render_sidebar()
st.markdown("<div class='eyebrow'>LIVE WEB RESEARCH / FIELDNOTE</div>", unsafe_allow_html=True)
st.title("Think clearly.\nResearch deeply.")
st.markdown("<p class='hero-copy'>Give the system a question worth investigating. It will search for current evidence, read the most relevant source, write a structured brief, and challenge its own conclusions.</p>", unsafe_allow_html=True)
st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-kicker mono'>START A SESSION</div>", unsafe_allow_html=True)
topic = st.text_area("Research question", placeholder="Example: How is AI changing the web development market in 2026?", height=110, label_visibility="collapsed", key="topic_input")
suggestions = ["What are the most important climate technologies to watch in 2026?", "How is AI changing the web development market in 2026?", "What are the latest risks and opportunities in quantum computing?"]
st.caption("Try a direction")
suggestion_columns = st.columns(3)
for column, suggestion in zip(suggestion_columns, suggestions):
	with column:
		if st.button(suggestion, key=suggestion, use_container_width=True):
			st.session_state["topic_input"] = suggestion
			st.rerun()
run_research = st.button("Begin research", type="primary", use_container_width=True)
if run_research:
	if not topic.strip():
		st.warning("Add a research question before starting.")
	else:
		try:
			from src.pipelines.pipeline import run_research_pipeline
			with st.status("Research session in progress", expanded=True) as status:
				st.write("01 / Search: finding recent and reliable sources")
				st.write("02 / Read: selecting and extracting a primary source")
				st.write("03 / Write: drafting the research report")
				st.write("04 / Critique: reviewing evidence, structure, and clarity")
				state = run_research_pipeline(topic.strip())
				status.update(label="Research session complete", state="complete", expanded=True)
			st.session_state["research_state"] = state
			st.session_state["research_topic"] = topic.strip()
		except Exception as error:
			st.error("The research session could not be completed.")
			st.exception(error)
if "research_state" in st.session_state:
	render_results(st.session_state["research_state"], st.session_state["research_topic"])
else:
	st.markdown("<div class='empty-state'><strong>Your brief will appear here</strong><span>Search, synthesis, and critique in one considered workspace.</span></div>", unsafe_allow_html=True)