import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def DeepQlearning_plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Length')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


def save_DeepQlearning_plot(scores, mean_scores, filename="DQL_plot.png"):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Length')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.savefig(filename)


def plot_scores(scores, mean_score, min_score, max_score):
    if len(scores) == 0:
        print("Error: no scores available to plot.")
        return
    if mean_score is None or min_score is None or max_score is None:
        print("Error: mean, min, or max score is None.")
        return
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Length')
    step = len(scores) // 1000 if len(scores) // 1000 > 0 else 1
    scores = scores[0:len(scores):step]
    plt.plot(scores)
    plt.axhline(
        y=mean_score,
        color="orange",
        label=f"Mean ({mean_score:.2f})"
    )
    plt.axhline(
        y=min_score,
        color="red",
        linestyle="--",
        label=f"Min ({min_score:.2f})"
    )
    plt.axhline(
        y=max_score,
        color="green",
        linestyle="--",
        label=f"Max ({max_score:.2f})"
    )
    plt.legend()
    plt.show()
    plt.pause(5)
    plt.savefig("QL_plot.png")
