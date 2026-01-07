# from data_loader import load_persona_csv, load_persona_signals
# import json

def extract_persona_context(persona_json, selected_persona):
    context = {}
    for category in ["name", "age", "skin_type", "skin_issues", "prefered_brands"]:
        context[category] = selected_persona.get(category, [])
    
    for category in ["lifestyle", "preference", "purchase_pattern"]:
        context[category] = {}
        persona_name = selected_persona[category]
        persona_data = persona_json[category][persona_name]

        context[category] = {
            "decision_drivers": persona_data.get("decision_drivers", []),
            "dislikes": persona_data.get("dislikes", []),
            "reacts_to": persona_data.get("reacts_to", [])
        }

    return context


# if __name__ == "__main__":
#     persona_signals = load_persona_signals("data/persona_signals.json")
#     load_single_persona_data = load_persona_csv("data/고객_페르소나.csv", "박원상")

#     print(type(load_single_persona_data))
#     persona_context = extract_persona_context(persona_signals, load_single_persona_data)
#     # print(json.dumps(persona_context, ensure_ascii=False, indent=2, default=str))
#     lifestyle_texts = "".join(persona_context.get("lifestyle", "").get("decision_drivers", [])) + "".join(persona_context.get("lifestyle", "").get("reacts_to", []))

#     # lifestyle_texts = []
#     # for v in persona_context.get("lifestyle", {}).values():
#     #     decision_drivers = v.get("decision_drivers", [])
#     #     reacts_to = v.get("reacts_to", [])
#     #     lifestyle_texts.append(" ".join(decision_drivers + reacts_to))

#     print(lifestyle_texts) 