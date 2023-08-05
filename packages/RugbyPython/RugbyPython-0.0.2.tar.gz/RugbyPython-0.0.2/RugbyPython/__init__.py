def pitch(ax, linecolor, poles, polescolor, labels, labelalpha, shadows):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import matplotlib.patheffects as path_effects

    Pitch = Rectangle([0,0], width = 100, height = 75, fill = False)
    color = linecolor
    color2 = polescolor

    halfway = plt.vlines(50, 0, 70, color)
    bottom = plt.hlines(0, 0, 100, color)
    top = plt.hlines(70, 0, 100, color)
    
    #10 meter lines and 22s
    ten1 = plt.vlines(60, 0, 70, color, '--', alpha=0.5)
    ten2 = plt.vlines(40, 0, 70, color, '--', alpha=0.5)
    twentytwo1 = plt.vlines(22, 0, 70, color, '-')
    twentytwo2 = plt.vlines(78, 0, 70, color, '-')
    five1 = plt.vlines(5, 0, 70, color, '--', alpha=0.5)
    five2 = plt.vlines(95, 0, 70, color, '--', alpha=0.5)
    hfive1 = plt.hlines(5, 0, 100, color, '-', alpha=0.5)
    hfive2 = plt.hlines(65, 0, 100, color, '-', alpha=0.5)
    
    #end lines
    end1 = plt.vlines(0, 0, 70, color)
    end2 = plt.vlines(100, 0, 70, color)
    
    if labels == True:
        if shadows == True and labelalpha != False:
            ax.text(18, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color=color, path_effects=[path_effects.withSimplePatchShadow()])
            ax.text(74, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color, path_effects=[path_effects.withSimplePatchShadow()])
            ax.text(46, 32, '50', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color, path_effects=[path_effects.withSimplePatchShadow()])
        elif labelalpha != False: 
            ax.text(18, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color=color)
            ax.text(74, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color)
            ax.text(46, 32, '50', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color)
        
    
    if poles == True:
        if polescolor == False:
            polesa = plt.vlines(0, 30, 40, color, '-', alpha=1, linewidth=5)
            poles1 = plt.vlines(100, 30, 40, color, '-', alpha=1, linewidth=5)
        if polescolor != False:
            polesa = plt.vlines(0, 30, 40, color2, '-', alpha=1, linewidth=5)
            poles1 = plt.vlines(100, 30, 40, color2, '-', alpha=1, linewidth=5)


####################################################

def helper(function):
    function = function
    if function == 'pitch' or function == 'vertpitch':
        print('1 ~ Open a new python file.')
        print('2 ~ To import RugbyPy, type: from RugbyPython import *, also import matplotlib.pyplot')
        print('3 ~ Start setting up the axis and plot with: fig=plt.figure()')
        print('4 ~ Set the size of the figure as you wish: fig.set_size_inches(x, y)')
        print('5 ~ Add subplot(s): ax=fig.add_subplot(1,1,1)')
        print('7 ~ Enter the following line and customize as wanted: pitch(ax=ax, linecolor="black", poles=True, polescolor = False, labels=False, labelalpha = 0.4, shadows=False)')
    
    if function != 'pitch' and function != 'vertpitch':
        print('Error, function not found.')

####################################################
    
def vertpitch(ax, linecolor, poles, polescolor, labels, labelalpha, shadows):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, ConnectionPatch
    import matplotlib.patheffects as path_effects
    
    color = linecolor
    color2 = polescolor

    halfway = plt.hlines(50, 0, 70, color)
    bottom = plt.hlines(0, 0, 70, color)
    top = plt.hlines(100, 0, 70, color)

    #10 meter lines and 22s
    ten1 = plt.hlines(40, 0, 70, color, '--', alpha=0.5)
    ten2 = plt.hlines(60, 0, 70, color, '--', alpha=0.5)
    twentytwo1 = plt.hlines(22, 0, 70, color, '-')
    twentytwo2 = plt.hlines(78, 0, 70, color, '-')
    five1 = plt.hlines(5, 0, 70, color, '--', alpha=0.5)
    five2 = plt.hlines(95, 0, 70, color, '--', alpha=0.5)
    hfive1 = plt.vlines(5, 0, 100, color, '-', alpha=0.5)
    hfive2 = plt.vlines(65, 0, 100, color, '-', alpha=0.5)

    #end lines
    end1 = plt.vlines(0, 0, 100, color)
    end2 = plt.vlines(70, 0, 100, color)

    if labels == True:
        if shadows == True and labelalpha != False:
            ax.text(31, 24, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color=color, path_effects=[path_effects.withSimplePatchShadow()])
            ax.text(31, 80, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color, path_effects=[path_effects.withSimplePatchShadow()])
            ax.text(31, 52, '50', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color, path_effects=[path_effects.withSimplePatchShadow()])
        elif labelalpha != False: 
            ax.text(31, 24, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color=color)
            ax.text(31, 80, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color)
            ax.text(31, 52, '50', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color)


    if poles == True:
        if polescolor == False:
            polesa = plt.hlines(100, 30, 40, color, '-', alpha=1, linewidth=5)
            poles1 = plt.hlines(0, 30, 40, color, '-', alpha=1, linewidth=5)
        if polescolor != False:
            polesa = plt.hlines(100, 30, 40, color2, '-', alpha=1, linewidth=5)
            poles1 = plt.hlines(0, 30, 40, color2, '-', alpha=1, linewidth=5)