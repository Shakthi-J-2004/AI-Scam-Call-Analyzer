import streamlit as st

def render_risk_score(score: int):
    color = "#00FFA3"
    shadow = "rgba(0, 255, 163, 0.4)"
    if score > 70:
        color = "#FF3366"
        shadow = "rgba(255, 51, 102, 0.5)"
    elif score > 30:
        color = "#FFD166"
        shadow = "rgba(255, 209, 102, 0.4)"
        
    st.markdown(f"""
        <div style="background: rgba(18, 24, 38, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); padding:30px; border-radius:16px; text-align:center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <p style="font-size:18px; color:#A0AEC0; margin:0; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Scam Risk Score</p>
            <h1 style="font-size:72px; color:{color}; margin:10px 0; font-weight: 800; text-shadow: 0 0 20px {shadow};">{score}</h1>
            <div style="width: 100%; background: #1E293B; border-radius: 10px; height: 12px; margin-top: 15px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);">
                <div style="width: {score}%; background: linear-gradient(90deg, {color}88 0%, {color} 100%); height: 100%; border-radius: 10px; box-shadow: 0 0 15px {color};"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_scam_type(scam_type: str, confidence: int):
    st.markdown(f"""
        <div style="background: rgba(18, 24, 38, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); padding:24px; border-radius:16px; margin-top:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color:#A0AEC0; margin: 0 0 5px 0; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 1px;">Detected Vector</h4>
                    <h3 style="color:#00FFA3; margin:0; font-weight: 800; font-size: 24px;">{scam_type}</h3>
                </div>
                <div style="text-align: right;">
                    <p style="color:#A0AEC0; margin:0; font-size: 12px; text-transform: uppercase;">Confidence</p>
                    <h2 style="color:#00B8FF; margin:0; font-weight: 800; text-shadow: 0 0 10px rgba(0, 184, 255, 0.4);">{confidence}%</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_flagged_transcript(flagged_sentences: list):
    st.markdown("<h3 style='margin-bottom: 20px; font-weight: 800; color: #F8FAFC;'>Transcript Analysis</h3>", unsafe_allow_html=True)
    
    html_content = '<div style="background: rgba(18, 24, 38, 0.4); border: 1px solid rgba(255,255,255,0.05); padding:25px; border-radius:16px; line-height: 1.8; font-size: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">'
    for item in flagged_sentences:
        text = item["text"]
        level = item["risk_level"]
        reason = item["reason"]
        
        if level == "Red":
            bg_color = "rgba(255, 51, 102, 0.15)"
            border_color = "#FF3366"
            text_color = "#FF8A9F"
        elif level == "Yellow":
            bg_color = "rgba(255, 209, 102, 0.15)"
            border_color = "#FFD166"
            text_color = "#FFE18F"
        else:
            bg_color = "transparent"
            border_color = "transparent"
            text_color = "#CBD5E1"
            
        if level in ["Red", "Yellow"]:
            html_content += f'<span style="background-color:{bg_color}; color: {text_color}; border-bottom: 2px solid {border_color}; padding:2px 4px; border-radius:4px; cursor: help; transition: all 0.2s ease;" title="{reason}">{text} </span>'
        else:
            html_content += f'<span style="color:{text_color}; padding: 2px;">{text} </span>'
            
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)

    with st.expander("View AI Insights & Explanations"):
        for item in flagged_sentences:
            if item["risk_level"] in ["Red", "Yellow"]:
                icon = "🔴" if item["risk_level"] == "Red" else "🟡"
                st.markdown(f"**{icon} flagged:** \"_{item['text']}_\"  \n**AI Insight:** {item['reason']}")

def render_recommendation(recommendation: str, summary: str):
    st.markdown(f"""
        <div style="background: linear-gradient(145deg, rgba(18, 24, 38, 0.8) 0%, rgba(9, 11, 16, 0.9) 100%); border-left: 4px solid #00B8FF; padding:24px; border-radius:16px; margin-top:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <h4 style="color:#00B8FF; margin-top:0; margin-bottom: 10px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">Action Recommendation</h4>
            <p style="color:#F8FAFC; font-size:16px; font-weight: 600;">{recommendation}</p>
            <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 20px 0;">
            <p style="color:#00FFA3; font-size:12px; margin-bottom:5px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Explain Like I'm 10</p>
            <p style="color:#94A3B8; font-size:15px; margin-bottom: 0;">{summary}</p>
        </div>
    """, unsafe_allow_html=True)
