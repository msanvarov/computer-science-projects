### Description

From an early draft of his Canterbury tales, Chaucer removed an account of the pilgrims staying at Anne Hoy’s inn, an establishment that served bad ale, but good cheese. The missing account explained how Anne kept her high-quality cheese stacked on stools, the largest rounds underneath the smaller rounds, to stop rats and mice from getting at them.
Occasionally the stool holding the cheese would need some maintenance (for example, the legs would start to buckle under the weight), and Anne would shift the entire stack from one stool to another. Since she could only move a single (hundred-pound plus) round of cheese at one time, and she refused to stack a larger-diameter cheese round on a smaller one (the outer part of the larger cheese would droop) she used three stools: one was her destination for her entire stack of cheese, one was the source (which likely needed its legs reinforced), and the third was for intermediate stacking. Chaucer immortalized the complicated routine Anne endured, lugging rounds of cheese from stool to stool as “The tour of Anne Hoy “ (TOAH).
One of Chaucer’s pilgrims had a mathematical bent. She had seen a miraculous early draft of the
Wikipedia article on the Tower of Hanoi in a vision, and noticed that Anne’s routine for moving cheeses was identical to the problem of moving rings between three posts. Using this similarity she calculated that to move n cheeses in this way required 2n 1 moves. This disheartened Anne, who had plans to increase her stack of cheese beyond the 8 she currently had. She decided to invest some of her prots in a fourth stool.
Anne gured that she could do substantially better than ```2^n-1``` moves using the following strategy:

* For a stack of 1 cheese round, her four-stool conguration allowed her to move the stack in 1 move, using her previous three-stool TOAH method.
* To move a stack of ```n > 1``` cheese rounds from some origin stool to some destination stool, she reasoned that she could think of some number ```i between 1 and n - 1```, and then:
    * Move ```n - i``` cheese rounds to an intermediate stool using all four stools.
    * Move i cheese rounds from the origin stool to the destination stool, using the (now) only three available stools and her TOAH method.
    * Move the ```n - i``` smallest cheese rounds from the intermediate stool to the destination stool, using all four stools

Notice that steps 1 and 3 require Anne to know how to move n i cheese rounds using four stools. Anne gured this wasn’t a problem, since she could apply her recursive strategy to this smaller problem. She presented her plan to the above-mentioned mathematically-inclined pilgrim who said that if she called the minimum number of moves that her strategy needed to move n rounds of cheese ```M(n)```, and if some ```i between 1 and n - 1``` were chosen.

After experimenting a bit Anne found she could move 3 cheese rounds in 5 moves (a little better than the 7 required by the TOAH method), and 6 cheese rounds in 17 moves much better than the 63 required by the TOAH method. But the choice of i made all the dierence. She (and the aforementioned math-geek pilgrim, who had decided to stay at her inn permanently) spent many hours with early prototypes of pencil and paper, guring out the best strategies for moving ever-larger stacks of cheese.
This is where matters stood, for centuries, until the invention of the computer.


### Application
The Tour of Anne Hoy Game is to move a stack of cheeses from the rst stool to the last stool, using only valid moves as described in the previous paragraphs.

### Dependencies
* python-ta (optional)


### Deployment
* Main Files: toah_model.py, tour.py, console_controller.py
* Graphical Dependicies: gui_******.py
* PYTA Files: tour_pyta.txt, toahmodel_pyta.txt, consolecontroller_pyta.txt
* To compile, execute the tour.py file.

### Changing Settings
* In the toah.py file under the ```if __name__ == '__main__'```, ```num_cheeses, and delay_between_moves``` can be altered to the users liking
