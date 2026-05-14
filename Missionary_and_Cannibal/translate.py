import json
import os

with open('missionary and cannibal.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

replacements = {
    '## Define the required library': '## 定义所需的库',
    '## load images': '## 加载图像',
    'In this section, external image files are loaded into the program to represent the visual elements of the game.': '在本节中，将外部图像文件加载到程序中以表示游戏的视觉元素。',
    'Three images are used: one for the boat, one for the missionary (human), and one for the cannibal (zombie). ': '使用了三张图像：一张代表船，一张代表传教士（人类），一张代表食人族（僵尸）。',
    'These images are read using matplotlib.image.imread, which converts the image files into arrays that can be displayed within the plot. ': '使用 matplotlib.image.imread 读取这些图像，这会将图像文件转换为可以在图表中显示的数组。',
    'This approach allows the game to have a more visual and engaging interface compared to using simple text or shapes.': '与使用简单的文本或形状相比，这种方法使游戏具有更直观和吸引人的界面。',
    '## game state': '## 游戏状态',
    'The game state defines the current configuration of the game at any point in time. ': '游戏状态定义了游戏在任何时间点的当前配置。',
    'It keeps track of the number of missionaries and cannibals on both the left and right sides of the river, as well as the boat’s position using the variable boat_x. ': '它跟踪河流左右两侧的传教士和食人族的数量，并使用变量 boat_x 记录船的位置。',
    'This state is updated after each valid move and is used to determine the game’s progress. ': '在每次有效移动后，此状态都会更新，并用于确定游戏的进度。',
    'Maintaining a clear game state ensures that the rules of the game are consistently enforced.': '保持清晰的游戏状态可确保始终如一地执行游戏规则。',
    '## IMAGE HELPER': '## 图像辅助函数',
    'The image helper function is used to place and display character images (missionaries and cannibals) on the plot at specific positions.': '图像辅助函数用于在图表的特定位置放置和显示角色图像（传教士和食人族）。',
    'It uses OffsetImage and AnnotationBbox to insert images at given coordinates with a defined size.': '它使用 OffsetImage 和 AnnotationBbox 将图像以定义的大小插入到给定的坐标处。',
    'This allows the images to be positioned precisely within the game scene. ': '这使得图像能够精确地定位在游戏场景中。',
    'By using this helper, the code avoids repetition and keeps the visualization process clean and organized.': '通过使用这个辅助函数，代码避免了重复，并保持了可视化过程的整洁和有序。',
    '## DRAW SCENE': '## 绘制场景',
    'The draw_scene function is responsible for rendering the entire game environment at each step.': 'draw_scene 函数负责在每一步渲染整个游戏环境。',
    'It draws the river, the two land areas, the boat, and all missionaries and cannibals based on the current game state. ': '它根据当前的游戏状态绘制河流、两块陆地、船以及所有的传教士和食人族。',
    'The function uses the stored values of the variables to position each element correctly on the screen. ': '该函数使用存储的变量值将每个元素正确地放置在屏幕上。',
    'This ensures that the visual representation is always synchronized with the game’s state.': '这确保了视觉表现始终与游戏状态保持同步。',
    '## Animation': '## 动画',
    'The animation function controls the smooth movement of the boat between the left and right sides of the river.': '动画函数控制船只在河流左右两侧之间的平滑移动。',
    'It updates the boat’s position gradually over several steps, creating the effect of motion instead of instant jumping.': '它在几个步骤中逐渐更新船的位置，从而产生运动效果，而不是瞬间跳跃。',
    'During the animation, the scene is continuously redrawn to reflect the updated boat position.': '在动画过程中，场景会不断重绘以反映更新后的船只位置。',
    'This provides a more realistic and visually appealing transition between states.': '这为状态之间提供了更真实、更具视觉吸引力的过渡。',
    '## Game logic': '## 游戏逻辑',
    'The game logic controls how players interact with the game and ensures that all moves follow the defined rules. ': '游戏逻辑控制玩家如何与游戏交互，并确保所有移动都遵循定义的规则。',
    'It checks whether the selected number of missionaries and cannibals is valid and updates their positions based on the boat’s movement. ': '它检查所选的传教士和食人族数量是否有效，并根据船的移动更新他们的位置。',
    'The logic also determines whether a move results in a win or a loss by evaluating the number of missionaries and cannibals on each side. ': '该逻辑还通过评估每侧传教士和食人族的数量来确定一步移动是否会导致胜利或失败。',
    'This ensures the game progresses correctly and enforces the constraints of the problem.': '这确保了游戏正确进行并强制执行问题的约束条件。',
    '## create solver button': '## 创建求解器按钮',
    'the solution is provided with bfs algorithm': '使用 BFS（广度优先搜索）算法提供解决方案',
    '## User Interface design': '## 用户界面设计',
    'The UI design provides an interactive interface for the player using buttons to select different move combinations. ': 'UI 设计通过使用按钮选择不同的移动组合，为玩家提供了一个交互式界面。',
    'Each button corresponds to a valid action, such as moving one missionary or one cannibal across the river.': '每个按钮对应一个有效的动作，例如将一名传教士或一名食人族运过河。',
    'A reset button is also included to restart the game at any time.': '还包括一个重置按钮，以便随时重新开始游戏。',
    'This design makes the game easier to play and more user-friendly compared to manual input.': '与手动输入相比，这种设计使游戏更容易玩，也更人性化。',
    '## Display: Run the simulation': '## 显示：运行模拟',
    'The display section is responsible for rendering the user interface elements and the game output in the Jupyter Notebook.': '显示部分负责在 Jupyter Notebook 中渲染用户界面元素和游戏输出。',
    'It shows the interactive buttons and the output area where the game scene is updated after each move.': '它显示了交互式按钮和输出区域，在每次移动后，游戏场景都会在此区域更新。',
    'The use of IPython.display ensures that the visual components are refreshed dynamically. ': 'IPython.display 的使用确保了视觉组件的动态刷新。',
    'This allows the player to interact with the game in real time within the notebook environment.': '这允许玩家在笔记本环境中实时与游戏进行交互。',
    '## End of Assignment 3': '## 任务 3 结束',
    'please write what you have learned today from this tutorial': '请写下你今天从本教程中学到了什么',
    "boat_pos = 'Left'": "boat_pos = '左侧'",
    "boat_pos = 'Right'": "boat_pos = '右侧'",
    'Boat position: {boat_pos} | Step {step}': '船的位置: {boat_pos} | 步数 {step}',
    '❌ Invalid move': '❌ 无效移动',
    '💀 YOU LOSE': '💀 你输了',
    '🎉 YOU WIN': '🎉 你赢了',
    'No solution found': '未找到解决方案',
    'Solving...': '求解中...',
    '🔄 Reset': '🔄 重置',
    '🤖 Auto Solve': '🤖 自动求解'
}

for cell in nb.get('cells', []):
    new_source = []
    for line in cell.get('source', []):
        for k, v in replacements.items():
            if k in line:
                line = line.replace(k, v)
        new_source.append(line)
    cell['source'] = new_source

with open('missionary and cannibal.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Translation completed successfully.')
