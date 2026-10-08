
# Predictive Banking Marketing Intelligence  Dashboard
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Predictive Banking Marketing Intelligence",
                   page_icon="🏦", layout="wide")

DEPTHS = [5, 10, 20, 30, 40, 50, 100]
FEATURE_LABELS = {
    "euribor3m": "3-Month Interest Rate",
    "nr.employed": "Employment Level",
    "days_since_previous_contact": "Days Since Previous Contact",
    "previously_contacted": "Previously Contacted",
    "emp.var.rate": "Employment Change Rate",
    "cons.conf.idx": "Consumer Confidence",
    "poutcome_success": "Previous Campaign Success",
    "age": "Customer Age",
    "cons.price.idx": "Consumer Price Index",
    "campaign_capped": "Number of Campaign Contacts",
    "previous": "Previous Contacts",
    "poutcome_nonexistent": "No Previous Campaign Outcome",
    "contact_telephone": "Telephone Contact",
    "month_may": "Contacted in May",
    "month_mar": "Contacted in March",
}
 
BLUE, DBLUE, ORANGE, NAVY = "#3B8FF3", "#0B5ED7", "#FF5A00", "#16365C"

st.markdown(f"""
<style>
header[data-testid="stHeader"] {{display:none;}}
.block-container {{padding:0.6rem 1rem 0.5rem 1rem; max-width:1500px;}}
[data-testid="stVerticalBlock"] {{gap:0.55rem;}}
[data-testid="stMarkdownContainer"] p {{margin:0;}}
label p {{font-size:12.5px !important;font-weight:700 !important;color:#16365C;}}
[data-testid="stWidgetLabel"] {{margin-bottom:-2px !important; min-height:0 !important;}}
div[data-baseweb="select"] > div, div[data-testid="stNumberInput"] input {{min-height:34px;}}

.banner {{background:linear-gradient(90deg,#14305A,#1B3A66);border-radius:6px;padding:6px 16px;
  display:grid;grid-template-columns:50px 1fr 250px;align-items:center;color:#fff;}}
.banner .ico {{font-size:30px;line-height:1;}}
.banner .mid {{text-align:center;}}
.banner h1 {{color:#fff;font-size:23px;margin:0 0 2px 0;font-weight:800;padding:0;line-height:1.25;}}
.banner .sub {{font-size:12px;color:#DCE7F5;line-height:1.3;}}
.goal {{border:1px solid #4A6A99;border-radius:6px;padding:4px 8px;font-size:10.5px;
  color:#DCE7F5;background:rgba(255,255,255,.07);line-height:1.35;}}

.kpi {{border-radius:8px;padding:8px 14px;min-height:84px;display:flex;gap:12px;align-items:center;}}
.kpi .t {{font-weight:700;font-size:13px;line-height:1.3;}}
.kpi .v {{font-weight:800;font-size:24px;line-height:1.25;}}
.kpi .s {{font-size:11px;line-height:1.3;}}

.h {{font-size:18px;font-weight:700;color:{NAVY};line-height:1.4;margin-bottom:2px;}}
.hs {{font-size:12px;color:#4A5A6A;line-height:1.4;}}
.outcome {{background:#E6F7EC;border-radius:4px;padding:4px 12px;margin-top:14px;line-height:1.3;}}
.outcome b {{font-size:14px;color:#1B7F3B;}} .outcome span {{font-size:11.5px;color:#2E5E3E;}}

.card {{border-radius:8px;text-align:center;padding:12px 4px;min-height:150px;}}
.card .i {{font-size:24px;line-height:1.3;}}
.card .t {{font-weight:800;font-size:12px;line-height:1.4;}}
.card .v {{font-weight:900;font-size:20px;line-height:1.3;}}
.card .s {{font-size:12px;color:#333;line-height:1.35;}}
.note {{font-size:11.5px;color:#667788;margin-top:6px;margin-bottom:10px;}}

.take-box {{background:#F4F8FE;border:1px solid #DDE7F5;border-radius:6px;padding:8px 12px;}}
.take {{display:flex;gap:10px;margin:6px 0;font-size:12.5px;color:#222;align-items:flex-start;line-height:1.4;}}
.take .n {{background:#1F6FEB;color:#fff;border-radius:50%;min-width:20px;height:20px;display:flex;
  align-items:center;justify-content:center;font-weight:700;font-size:12px;flex-shrink:0;margin-top:1px;}}

table.t {{width:100%;border-collapse:collapse;font-size:12px;}}
table.t th {{background:#F1F4F9;text-align:left;padding:5px 6px;border:1px solid #DDE3EC;color:#222;}}
table.t td {{padding:4px 6px;border:1px solid #E6EAF0;color:#222;white-space:nowrap;}}
.pill {{background:#BFEBC9;color:#1B7F3B;border-radius:10px;padding:1px 14px;font-weight:600;}}
</style>
""", unsafe_allow_html=True)


def html(s):
    """Collapse whitespace so Markdown never mis-parses indented HTML."""
    st.markdown(" ".join(s.split()), unsafe_allow_html=True)


def html_in(col, s):
    col.markdown(" ".join(s.split()), unsafe_allow_html=True)


@st.cache_data
def load():
    return (pd.read_csv("customer_priority_dashboard.csv"),
            pd.read_csv("contact_depth_analysis.csv"),
            pd.read_csv("feature_importance.csv"))


cust, depth, feat = load()
depth["Contact Depth (%)"] = depth["Contact Depth (%)"].astype(int)
depth = depth[depth["Contact Depth (%)"].isin(DEPTHS)].sort_values("Contact Depth (%)").copy()
total = len(cust)
rate = cust["Actual_Subscription"].mean()
opts = depth["Contact Depth (%)"].tolist()
rec = 20 if 20 in opts else opts[0]
recrow = depth[depth["Contact Depth (%)"] == rec].iloc[0]

# HEADER 
html("""
<div class="banner">
  <div class="ico">🏛️</div>
  <div class="mid">
    <h1>Predictive Banking Marketing Intelligence</h1>
    <div class="sub">Target the Right Customers &nbsp;|&nbsp; Increase Term Deposit Subscriptions &nbsp;|&nbsp; Use Marketing Resources Efficiently</div>
  </div>
  <div class="goal"><b>🎯 Goal</b><br>Identify and contact customers most likely to subscribe to a term deposit before the call.</div>
</div>""")


# KPI helper 
def kpi(col, bg, color, title, value, sub, icon):
    html_in(col, f"""<div class="kpi" style="background:{bg}">
    <div style="font-size:26px">{icon}</div>
    <div><div class="t" style="color:{color}">{title}</div>
    <div class="v" style="color:{color}">{value}</div>
    <div class="s" style="color:{color}">{sub}</div></div></div>""")


def card(col, bg, color, icon, title, val, sub):
    html_in(col, f"""<div class="card" style="background:{bg}"><div class="i">{icon}</div>
    <div class="t" style="color:{color}">{title}</div>
    <div class="v" style="color:{color}">{val}</div><div class="s">{sub}</div></div>""")


# LEFT: OPTIMIZATION + CHART + CONTACT LIST | RIGHT: KPIs + FEATURES + TAKEAWAYS
left, right = st.columns([1.7, 1], gap="medium")

with left:
    html('<div class="h" style="font-size:23px;margin-top:16px">Marketing Optimization</div>'
         '<div class="hs" style="font-size:13.5px;margin-bottom:12px">Choose the contact percentage and adjust the inputs to compare targeting results, costs, and expected business value.</div>')
    a_, b_, c_, d_ = st.columns([0.8, 0.8, 0.8, 1.6], gap="small")
    sel = a_.selectbox("Customers to Target", opts, index=opts.index(rec), format_func=lambda x: f"{x}%")
    cost_per_call = b_.number_input("Cost / Call ($)", min_value=0.0, value=5.0, step=1.0)
    value_per_sub = c_.number_input("Est. Value per Subscriber($)", min_value=0.0, value=100.0, step=10.0)

    row = depth[depth["Contact Depth (%)"] == sel].iloc[0]
    n_contact = int(row["Customers Contacted"])
    subs = int(row["Subscribers Captured"])
    cap = float(row["Subscribers Captured (%)"])
    lift = float(row["Lift"])
    avoided = total - n_contact
    savings = avoided * cost_per_call
    net = subs * value_per_sub - n_contact * cost_per_call
    html_in(d_, f"""<div class="outcome"><b>Targeting Scenario (Top {sel}%)</b><br>
    <span>Historical results and estimated business impact for {n_contact:,} contacts.</span></div>""")

    html('<div style="height:14px"></div>')   
    cc = st.columns(6)
    card(cc[0], "#EAFBF0", "#1B7F3B", "👥", "Subscribers Reached", f"{subs:,}", f"({cap:.0f}% of all subscribers)")
    card(cc[1], "#FFF1E0", "#E8590C", "☎️", "Customers to Contact", f"{n_contact:,}", f"Top {sel}% of evaluation contacts")
    card(cc[2], "#EAF1FD", "#1F6FEB", "📞", "Calls Avoided", f"{avoided:,}", f"({avoided / total:.0%} reduction)")
    card(cc[3], "#FFF6DD", "#B7791F", "🏷️", "Call-Cost Savings", f"${savings:,.0f}", f"${cost_per_call:,.0f} × calls avoided")
    card(cc[4], "#E9F7EF", "#1B7F3B", "💰", "Estimated Campaign Value", f"${net:,.0f}", f"(${value_per_sub:,.0f}/sub minus cost)")
    card(cc[5], "#EFEAFD", "#5B2FD0", "📊", "Improvement vs. Random Targeting", f"{lift:.1f}x", "More effective at reaching subscribers")
    html('<div class="note">Cost per call and value per subscription are user-defined assumptions for scenario analysis; they are not part of the original dataset.</div>')

    # bar chart 
    
    depth["Net"] = (
        depth["Subscribers Captured"] * value_per_sub
        - depth["Customers Contacted"] * cost_per_call
    )
    
    html(
        '<div class="h" style="margin-top:16px">'
        'Campaign Value & Subscriber Capture by Contact Level'
        '</div>'
        '<div class="hs" style="margin-top:3px;margin-bottom:10px">'
        'Compare estimated net value with the percentage of subscribers reached at each contact level.'
        '</div>'
    )

    x = depth["Contact Depth (%)"].astype(str) + "%"
    colors = [DBLUE if d_v == sel else BLUE for d_v in depth["Contact Depth (%)"]]

    fig = go.Figure()

    fig.add_bar(
        x=x,
        y=depth["Net"],
        marker_color=colors,
        name="Estimated Net Campaign Value",
        text=[f"<b>${v / 1000:,.0f}K</b>" for v in depth["Net"]],
        textposition="inside",
        insidetextanchor="start",
        textfont=dict(color="white", size=14))

    fig.add_scatter(
        x=x,
        y=depth["Subscribers Captured (%)"] / 100,
        name="Subscribers Reached",
        yaxis="y2",
        mode="lines+markers",                      
        line=dict(color=ORANGE, width=3),
        marker=dict(size=9, color=ORANGE, line=dict(color="white", width=1.5))
    )

    # Labels in white boxes so they stay readable on top of the blue bars
    for xi, v in zip(x, depth["Subscribers Captured (%)"]):
        fig.add_annotation(
            x=xi, y=v / 100, xref="x", yref="y2",
            text=f"<b>{v:.0f}%</b>",
            showarrow=False, yshift=15,
            font=dict(color=ORANGE, size=12),
            bgcolor="white", bordercolor=ORANGE, borderwidth=1, borderpad=1
        )

    fig.update_layout(
        height=270,
        margin=dict(l=15, r=15, t=45, b=55),
        plot_bgcolor="white",
        xaxis=dict(
            type="category",
            title="Customers Contacted (% of Evaluation Group)"
        ),
        yaxis=dict(
            title="Estimated Net Campaign Value ($)",
            rangemode="tozero"
        ),
        yaxis2=dict(
            title="Subscribers Reached (%)",
            overlaying="y",
            side="right",
            range=[0, 1.2],
            tickformat=".0%",
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            x=0.50,
            y=1.16
        ),
        bargap=0.35,
        font=dict(size=11)
    )

    st.plotly_chart(fig, use_container_width=True)    

    # contact list 
    top = cust.sort_values("Predicted_Probability", ascending=False).head(n_contact).copy()
    download_df = top.drop(
        columns=[
            "Actual_Subscription",
            "Recommended_Contact",
            "Rank_Percentage"
        ],
        errors="ignore"
    ).rename(
        columns={"Predicted_Probability": "Priority_Score"}
    )
    h1, h2 = st.columns([1.6, 1], gap="small")
    with h1:
        html(f'<div class="h">Priority Contacts</div>'
             f'<div class="hs" style="margin-top:2px">{len(top):,} contacts in the selected list; the download contains all of them.</div>')
    with h2:
        st.download_button("⬇ Download Priority Contact List", download_df.to_csv(index=False).encode("utf-8"),
                           f"priority_customers_top_{sel}_percent.csv", "text/csv",
                           use_container_width=True)
    pref = [c for c in ["age", "job", "education", "poutcome"] if c in top.columns]
    if not pref:
        pref = [c for c in top.columns if c not in
                {"Predicted_Probability", "Actual_Subscription", "Customer_Rank", "Customer_ID"}][:3]
    rows = ""
    for i, (_, r) in enumerate(top.head(5).iterrows(), 1):
        cid = r["Customer_ID"] if "Customer_ID" in top.columns else f"C_{r.name}"
        rank = int(r["Customer_Rank"]) if "Customer_Rank" in top.columns else i
        chars = ", ".join(f"{c}: {str(r[c])[:12]}" for c in pref[:3])
        rows += (f"<tr><td>{rank}</td><td>{cid}</td><td>{r['Predicted_Probability']:.2f}</td>"
                 f"<td>{chars}</td><td><span class='pill'>Contact</span></td></tr>")
    html(f"""<table class="t"><tr><th>Rank</th><th>Customer ID</th><th>Priority Score</th>
    <th>Key Characteristics</th><th>Action</th></tr>{rows}</table>""")

with right:
    html('<div style="height:36px"></div>')
    k1, k2 = st.columns(2)
    kpi(k1, "#E8F1FD", "#111", "Evaluation Contacts", f"{total:,}", "Contacts used to evaluate the model", "👥")
    kpi(k2, "#E6F7EC", "#1B7F3B", "Historical Subscription Rate", f"{rate:.1%}", "Subscribed to term deposit", "📶")

    html('<div class="h" style="margin-top:16px;padding-left:25px">Key Drivers of Subscription</div>'
         '<div class="hs" style="padding-left:25px;margin-bottom:16px">Factors the model found most useful for identifying likely subscribers</div>')
    f = feat.head(10).sort_values("Importance").copy()
    f["Feature"] = f["Feature"].map(lambda v: FEATURE_LABELS.get(v, v))  
    fig = go.Figure(go.Bar(x=f["Importance"], y=f["Feature"], orientation="h", marker_color=BLUE,
                           text=f["Importance"].round(2), textposition="outside"))
    fig.update_layout(height=290, margin=dict(l=25, r=25, t=5, b=0),
                      xaxis=dict(range=[0, max(0.3, f["Importance"].max() * 1.3)]), plot_bgcolor="white",
                      font=dict(size=11))
    _pad, chart_col = st.columns([0.1, 0.9])
    chart_col.plotly_chart(fig, use_container_width=True)

    # extra KPIs 
    call_cost = n_contact * cost_per_call
    cost_per_sub = call_cost / subs if subs else 0
    roi = f"{net / call_cost:,.1f}x" if call_cost > 0 else "N/A"
 
    e1, e2 = st.columns(2)
    kpi(e1, "#FFF6DD", "#B7791F", "Cost per Subscription", f"${cost_per_sub:,.2f}", f"vs ${value_per_sub:,.0f} value each", "🧾")
    kpi(e2, "#E6F7EC", "#1B7F3B", "Return on Investment", roi, "net value ÷ calling cost", "📈")
    html('<div style="height:26px"></div>')   
 
    # Find the contact level with the highest estimated campaign value
    best = depth.loc[depth["Net"].idxmax()]
    best_d = int(best["Contact Depth (%)"])

    # Compare selected level with the previous contact level
    d_list = depth["Contact Depth (%)"].tolist()
    i_sel = d_list.index(sel)

    if i_sel > 0:
        prev = depth.iloc[i_sel - 1]
        prev_d = int(prev["Contact Depth (%)"])
        add_subs = subs - int(prev["Subscribers Captured"])
        add_calls = n_contact - int(prev["Customers Contacted"])
        marg = add_subs / add_calls if add_calls else 0
        t2 = (
            f"Expanding targeting from <b>{prev_d}%</b> to <b>{sel}%</b> reached "
            f"<b>{add_subs:,} additional subscribers</b> with "
            f"<b>{add_calls:,} additional calls</b>, representing a "
            f"<b>{marg:.1%} subscription rate</b> among those additional contacts."
        )
    else:
        t2 = (
            f"Targeting the top <b>{sel}%</b> focuses the campaign on the "
            f"highest-priority contacts."
        )

    total_subs = int(cust["Actual_Subscription"].sum())
    selected_rate = subs / n_contact * 100 if n_contact else 0
    overall_rate = rate * 100
    missed_subs = total_subs - subs

    if best_d == 20:
        t7 = "Under the current illustrative cost and value assumptions, <b>Top 20%</b> produces the highest estimated campaign value."
    elif best_d > 20:
        t7 = (f"Under the current illustrative cost and value assumptions, <b>Top {best_d}%</b> produces the highest estimated campaign value, "
              "while <b>Top 20%</b> needs fewer calls and remains the resource-efficient starting strategy.")
    else:
        t7 = (f"Under the current illustrative cost and value assumptions, <b>Top {best_d}%</b> produces the highest estimated campaign value; "
              "Top 20% captures more subscribers at a higher calling cost.")

    html(f"""<div class="take-box">
    <div class="h" style="color:#1F6FEB;font-size:16px">💡 Key Takeaways</div>

    <div class="take"><div class="n">1</div>
    <div>Targeting the Top {sel}% reaches <b>{subs:,}</b> historical subscribers, or <b>{cap:.0f}%</b> of all subscribers in the evaluation data.</div></div>

    <div class="take"><div class="n">2</div>
    <div>This requires contacting <b>{n_contact:,}</b> of the {len(cust):,} evaluation contacts, avoiding <b>{avoided:,}</b> calls compared with contacting the full evaluation set.</div></div>

    <div class="take"><div class="n">3</div>
    <div>Avoiding those calls represents approximately <b>${savings:,.0f}</b> in estimated call-cost savings under the current assumptions.</div></div>

    <div class="take"><div class="n">4</div>
    <div>The selected group has a <b>{selected_rate:.1f}%</b> historical subscription rate, compared with <b>{overall_rate:.1f}%</b> overall (<b>{lift:.2f}× lift</b> over random targeting).</div></div>

    <div class="take"><div class="n">5</div>
    <div><b>{missed_subs:,}</b> historical subscribers remain outside the selected Top {sel}%, so expanding the contact depth may reach more subscribers but requires additional calls.</div></div>

    <div class="take"><div class="n">6</div><div>{t7}</div></div>
</div>""")

# planning note
html("""<div class="note" style="margin-top:12px;padding:3px 10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:4px;line-height:1.2;">
<b>Planning note:</b> Results are based on historical campaign data and are intended to support marketing decisions. Future performance may vary as customer behavior and economic conditions change. Cost per call and estimated subscriber value are user-defined planning assumptions and are not part of the original dataset.
</div>""")
