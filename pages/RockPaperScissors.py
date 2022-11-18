import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

def heatmap(matrix, xticks, yticks):
    "Based on https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html"
    fig, ax = plt.subplots(figsize=(3,3))
    im = ax.imshow(matrix, cmap="Wistia")

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(xticks)), labels=xticks)
    ax.set_yticks(np.arange(len(yticks)), labels=yticks)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(yticks)):
        for j in range(len(xticks)):
            text = ax.text(j, i, matrix[i, j],
                        ha="center", va="center")
    fig.tight_layout()
    return fig

st.title("Rock Paper Scissors")

RPS_options = ("Rock", "Paper", "Scissors")

if "results" not in st.session_state:
    st.session_state.results = np.zeros([3,3], dtype=int)

tab1, tab2 = st.tabs(["Game", "Help"])

if "initial_choice" not in st.session_state:
    st.session_state.initial_choice = 0

with tab1:
    col11, col21, col31 = st.columns([5,1,1])
    if col21.button("Random"):
        st.session_state.initial_choice = random.randint(0,2)
    col31 = col31.empty()
    human_selection = col11.radio("Choose one of the following", RPS_options, horizontal=True, index=st.session_state.initial_choice)
    # Put some images
    col12, col22, col32 = st.columns([3,3,4])
    image_ph = col12.empty()
    image_ph.image(f"images/{human_selection}.png", width=200)
    col12.caption("Your choice")
    if col31.button("Play"):
        computer_selection = random.choice(RPS_options[:3])
        if human_selection == "Random":
            human_selection = random.choice(RPS_options[:3])
        image_ph.image(f"images/{human_selection}.png", width=200)
        # Convert to numbers and store
        hs_index = RPS_options.index(human_selection)
        cs_index = RPS_options.index(computer_selection)
        st.session_state.results[hs_index, cs_index] += 1
        # Who wins?
        if hs_index == cs_index:
            col22.title("It's a tie!")
        elif (hs_index + 1) % 3 == cs_index:
            col22.title("Computer wins!")
        else:
            col22.title("You win!")
        col32.image(f"images/{computer_selection}.png", width=200)
        col32.caption("Computer's choice")
    # Put some stats, and keep them all the time
    col13, col23, col33, col43 = st.columns([1,1,1,2])
    col13.metric("Wins", st.session_state.results[0,2] + st.session_state.results[1,0] + st.session_state.results[2,1])
    col23.metric("Ties", st.session_state.results[0,0] + st.session_state.results[1,1] + st.session_state.results[2,2])
    col33.metric("Losses", st.session_state.results[0,1] + st.session_state.results[1,2] + st.session_state.results[2,0])
    col43.pyplot(heatmap(st.session_state.results, [_+" (PC)" for _ in RPS_options[:3]], [_+" (You)" for _ in RPS_options[:3]]))

with tab2:
    st.write("In the remote case you don't know how to play, this is how it works:")
    st.write("You choose one of the three options, and the computer will choose one too.")
    st.write("Rock beats scissors, scissors beats paper, and paper beats rock.")
    st.write("More info on the [Wikipedia](https://en.wikipedia.org/wiki/Rock_paper_scissors), as usual. That's where the images come from!")
    st.write("Good luck!")