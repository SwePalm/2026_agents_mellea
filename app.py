from __future__ import annotations

import json
from typing import Any, List, Literal, TypedDict

import gradio as gr
import mellea
from mellea import generative


class CocktailRecipe(TypedDict):
    name: str
    vibe_match_score: int  # 1-100 score of how well it fits the user request
    glassware: Literal[
        "Coupe",
        "Highball",
        "Rocks",
        "Martini",
        "Mule Mug",
        "Nick and Nora",
    ]
    ingredients: List[str]  # Must include precise measurements
    instructions: List[str]
    garnish: str
    pro_tip: str  # A secret detail about the technique


session = mellea.start_session()


@generative
def generate_cocktail_recipe(m: Any, user_vibe: str) -> CocktailRecipe:
    """
    You are The Strict Mixologist, a world-class bartender and flavor architect.
    Given a user's vibe, create a precise cocktail recipe that matches the mood.

    Requirements:
    - Output must follow the CocktailRecipe schema exactly.
    - Provide a vivid, creative name.
    - vibe_match_score is an integer 1-100 indicating how well it fits the vibe.
    - glassware must be one of the allowed Literal values.
    - ingredients must include precise measurements (e.g., "1.5 oz gin").
    - instructions are concise, ordered steps.
    - garnish is a single, specific item.
    - pro_tip reveals a secret technique detail for excellence.

    User vibe:
    {user_vibe}
    """
    raise NotImplementedError("Generative slot: implemented by the Mellea runtime.")


def format_recipe(recipe: CocktailRecipe) -> str:
    return "\n".join(
        [
            "### The Strict Mixologist",
            f"**Name:** {recipe['name']}",
            f"**Vibe Match:** {recipe['vibe_match_score']}/100",
            f"**Glassware:** {recipe['glassware']}",
            "**Ingredients:**",
            "\n".join([f"- {item}" for item in recipe["ingredients"]]),
            "**Instructions:**",
            "\n".join([f"{idx}. {step}" for idx, step in enumerate(recipe["instructions"], 1)]),
            f"**Garnish:** {recipe['garnish']}",
            f"**Pro Tip:** {recipe['pro_tip']}",
            "",
            "```json",
            json.dumps(recipe, indent=2),
            "```",
        ]
    )


def generate(user_vibe: str) -> str:
    recipe = generate_cocktail_recipe(session, user_vibe)
    return format_recipe(recipe)


with gr.Blocks(title="The Strict Mixologist") as demo:
    gr.Markdown("# The Strict Mixologist")
    gr.Markdown(
        "A Mellea-powered generative computing demo: structured cocktail recipes with zero prompt soup."
    )

    vibe_input = gr.Textbox(
        label="Vibe",
        placeholder="A rainy Tuesday in a London jazz club",
    )
    generate_button = gr.Button("Generate")
    output = gr.Markdown()

    generate_button.click(fn=generate, inputs=vibe_input, outputs=output)


if __name__ == "__main__":
    demo.launch()
