# ----- DSI Functions ----- #
def get_at_time(df, t, time_label):
    """
    Slice df which is a multi index dataframe
    use this function to get the element at time t of each sample
    if t = -1 then it will be the last element
    """
    import numpy as np
    import pandas as pd
    dft = {}
    sample_index = list(df.index.levels[0])
    no_sams = len(sample_index)

    if t == -1:
        for i in range(no_sams):
            dft[i] = df.loc[i].iloc[-1]
    else:
        for i in range(no_sams):
            sliced = df.loc[i][df.loc[i][time_label].round() == np.round(t)]
            if sliced.size == 0:
                pass
            else:
                dft[i] = sliced.iloc[0]
    return pd.DataFrame(dft).T

class DSI_3D():
    """
    Design space identification framework
    Takes in df as input of labelled pandas DataFrame data
    """
    def __init__(self, df, labels, **kwargs):
        """
        Initialize internal definitions
        df: labelled pandas dataframe
        labels: dictionary containing keys: 'vnames': ['namevar1', 'namevar2', 'namevar3'] - names of variables varied
                                            'units': ['unitsvar1', 'unitsvar2', 'unitsvar3', 'unitsvolume']
        """
        # Try to import matlab engine. If not found, alpha shape of the design space cannot be calculated.
        try:
            import matlab.engine
            self.eng = matlab.engine.start_matlab() # Start instance of matlab engine
        except ModuleNotFoundError:
            self.eng = 'WARNING: matlab engine not found. Alpha shape of design space cannot be calculated.\nInstall from: https://uk.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html'
            print(self.eng)
            
        self.df = df
        self.labels = labels
        self.all_x = []
        self.all_fcube = []
        
        # ----- Set default cmap ----- #
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
        inferno_modified = plt.cm.get_cmap('inferno', 256)
        inferno80 = ListedColormap(inferno_modified(np.linspace(0, 0.8, 256)))

        gray_modified = plt.cm.get_cmap('gray', 256)
        self.gray80 = ListedColormap(gray_modified(np.linspace(0, 0.85, 256)))

        self.default_cmap = inferno80
        
        # ----- Unpacking options ----- #
        options = kwargs.get('options', None)
        # Internal definition
        self.options = options
        if options == None:
            self.hide_sat      = False
            self.hide_vio      = False
            self.hide_surf     = False
            self.step_change   = 1 # in percent
            self.tmark         = '.'
            self.tcolor        = 'blue'
            self.msize         = 30
            self.ccolor        = 'black'
            self.clinewidth    = 0.5
            self.alpha_points  = 0.5
            self.alpha_surface = 0.1
            self.leg           = True
            self.cmap          = self.default_cmap
            self.hmv = None
            self.gray_scale = False
            self.surfcolor  = 'g'
            self.satcolor   = 'g'
            self.viocolor   = 'r'
            self.satmarker  = 'o'
            self.viomarker  = 'o'
            self.npcolor    = 'blue'
            self.npmarker   = 'x'
            self.plot_lbd   = None
            self.plot_ubd   = None

        else:
            # Hide points
            self.hide_sat  = options.get('hidesat', False)
            self.hide_vio  = options.get('hidevio', False)
            self.hide_surf = options.get('hidesurf', False)
            # Cube params
            self.step_change = options.get('step_change', 1)
            self.tmark       = options.get('tmark', '.')
            self.tcolor      = options.get('tcolor', 'blue')
            self.msize       = options.get('msize', 30)
            self.ccolor      = options.get('ccolor', 'black')
            self.clinewidth  = options.get('clinewidth', 0.5)
            # Plotting options
            self.alpha_points  = options.get('alpha_points', 0.5)
            self.alpha_surface = options.get('alpha_surface', 0.1)
            self.leg           = options.get('leg', True)
            self.cmap          = options.get('cmap', self.default_cmap)
            self.hmv    = options.get('hmv', None)
            self.gray_scale    = options.get('gray_scale', False)
            self.surfcolor     = options.get('surfcolor', 'g')
            self.satcolor      = options.get('satcolor', 'g')
            self.viocolor      = options.get('viocolor', 'r')
            self.npcolor       = options.get('npcolor', 'blue')
            self.satmarker     = options.get('satmarker', 'o')
            self.viomarker     = options.get('viomarker', 'o')
            self.npmarker      = options.get('npmarker', 'x')  
            self.plot_ubd      = options.get('plot_ubd', None)
            self.plot_lbd      = options.get('plot_lbd', None)
        # Gray scale plotting template
        if self.gray_scale:
            self.cmap = self.gray80
            self.tcolor = 'black'
            self.surfcolor = 'grey'
            self.alpha_surface = 0.3
            self.satcolor = 'black'
            self.viocolor = 'black'
            self.viomarker = 's' 
            self.npcolor = 'black'
            self.alpha_points = 0.5
            self.npmarker = 'x'
            self.msize = 30
            if self.hmv != None:
                self.alpha_surface = 0.1
                
    def update_options(self, options = None):
        """
        Update self options. If None then reset to default options.
        """
        # Internal definition
        self.options = options
        if options == None:
            self.hide_sat      = False
            self.hide_vio      = False
            self.hide_surf     = False
            self.step_change   = 1 # in percent
            self.tmark         = '.'
            self.tcolor        = 'blue'
            self.msize         = 30
            self.ccolor        = 'black'
            self.clinewidth    = 0.5
            self.alpha_points  = 0.5
            self.alpha_surface = 0.1
            self.leg           = True
            self.cmap          = self.default_cmap
            self.hmv = None
            self.gray_scale = False
            self.surfcolor  = 'g'
            self.satcolor   = 'g'
            self.viocolor   = 'r'
            self.satmarker  = 'o'
            self.viomarker  = 'o'
            self.npcolor    = 'blue'
            self.npmarker   = 'x'
            self.plot_lbd   = None
            self.plot_ubd   = None

        else:
            # Hide points
            self.hide_sat  = options.get('hidesat', False)
            self.hide_vio  = options.get('hidevio', False)
            self.hide_surf = options.get('hidesurf', False)
            # Cube params
            self.step_change = options.get('step_change', 1)
            self.tmark       = options.get('tmark', '.')
            self.tcolor      = options.get('tcolor', 'blue')
            self.msize       = options.get('msize', 30)
            self.ccolor      = options.get('ccolor', 'black')
            self.clinewidth  = options.get('clinewidth', 0.5)
            # Plotting options
            self.alpha_points  = options.get('alpha_points', 0.5)
            self.alpha_surface = options.get('alpha_surface', 0.1)
            self.leg           = options.get('leg', True)
            self.cmap          = options.get('cmap', self.default_cmap)
            self.hmv    = options.get('hmv', None)
            self.gray_scale    = options.get('gray_scale', False)
            self.surfcolor     = options.get('surfcolor', 'g')
            self.satcolor      = options.get('satcolor', 'g')
            self.viocolor      = options.get('viocolor', 'r')
            self.npcolor       = options.get('npcolor', 'blue')
            self.satmarker     = options.get('satmarker', 'o')
            self.viomarker     = options.get('viomarker', 'o')
            self.npmarker      = options.get('npmarker', 'x')  
            self.plot_ubd      = options.get('plot_ubd', None)
            self.plot_lbd      = options.get('plot_lbd', None)
        # Gray scale plotting template
        if self.gray_scale:
            self.cmap = self.gray80
            self.tcolor = 'black'
            self.surfcolor = 'grey'
            self.alpha_surface = 0.3
            self.satcolor = 'black'
            self.viocolor = 'black'
            self.viomarker = 's' 
            self.npcolor = 'black'
            self.alpha_points = 1
            self.npmarker = 'x'
            self.msize = 30
            if self.hmv != None:
                self.alpha_surface = 0.1

    def screen_points(self, constraints):
        """
        Takes in the DataFrame, data, and dictionary, constraints, giving out the satisfied and violated DataFrame of samples
        """
        data = self.df
        self.constraints = constraints
        sat = data.copy()
        for i in list(constraints.keys()):
            sat = sat[sat[i] <= constraints[i][0]]
            sat = sat[sat[i] >= constraints[i][1]]
        exclude_these = data.index.isin(list(sat.index))
        vio = data[~exclude_these]
        self.sat = sat
        self.vio = vio
        return sat, vio
        
    def inShape(self, x):
        """
        Check whether the point x lies within the shape in self.shp
        MATLAB function wrapper for ease of use.
        """
        import matlab.engine
        shp = self.shp
        return self.eng.inShape(shp, matlab.double(list(x)))
        
    def alphaShape(self, threeDdata):
        """
        Calculate the alphashape using the critical alpha (smallest alpha radius that envelopes all points).
        MATLAB function wrapper for ease of use.
        """
        import matlab.engine
        X = self.eng.transpose(matlab.double(list(threeDdata[:, 0])))
        Y = self.eng.transpose(matlab.double(list(threeDdata[:, 1])))
        Z = self.eng.transpose(matlab.double(list(threeDdata[:, 2])))
        shp = self.eng.alphaShape(X, Y, Z, nargout = 1)
        self.shp = shp
        return shp
    
    def plot(self):
        """
        Plotting 3D design space based on satisfied and violated points.
        alphaShape function in MATLAB is used to calculate the alpha shape and its volume.
        satisfied, violated, and the surface can be hidden by passing true or false of 'hide_sat', 
        'hide_vio', and 'hide_surf' in options
        """
        import numpy as np
        from matplotlib import pyplot as plt
        import matplotlib
        import pandas as pd
        
        # ----- External definitions ----- #
        sat = self.sat
        vio = self.vio
        labels = self.labels
        units  = labels.get('units',  ['[-]', '[-]', '[-]'])
        vnames = labels.get('vnames', ['x', 'y', 'z'])
        xlabe = vnames[0] + ' ' + '[' + units[0] + ']'
        ylabe = vnames[1] + ' ' + '[' + units[1] + ']'
        zlabe = vnames[2] + ' ' + '[' + units[2] + ']'
        
        # Alpha shape calculation using 
        points = sat[vnames].to_numpy()
        shp = self.alphaShape(points)
        self.eng.workspace['shp'] = shp
        vol = self.eng.volume(shp)
        tri, vert = self.eng.boundaryFacets(shp, nargout = 2)
        tri = np.array(tri).astype('int') - 1
        vert = np.array(vert)

        # 3D Create figure
        fig = plt.figure()
        ax = fig.add_subplot(projection = '3d')
        
        # If hmv: heatmap variable is available
        if self.hmv != None:
            if self.hide_sat:
                hmvdf = vio.copy()
            elif self.hide_vio:
                hmvdf = sat.copy()
            else:
                hmvdf = pd.concat([sat, vio], axis = 0)
            hmvdf = hmvdf[self.hmv]
            norm = matplotlib.colors.Normalize(vmin = hmvdf.min(), vmax = hmvdf.max())
            
            sm = plt.cm.ScalarMappable(cmap = self.cmap, norm = norm)
            fig.colorbar(sm, label = self.hmv)

            # ----- Calculating Heatmapvar values ----- #
            hmv_ave  = sat[self.hmv].mean()
            hmv_max  = sat[self.hmv].max()
            hmv_maxp = sat[sat[self.hmv] == hmv_max].to_string()
            hmv_min  = sat[self.hmv].min()
            hmv_minp = sat[sat[self.hmv] == hmv_min].to_string()
        else:
            hmv_ave  = None
            hmv_max  = None
            hmv_maxp = None
            hmv_min  = None
            hmv_minp = None
        
        # Plotting the samples
        if self.hide_sat == False:
            if self.hmv != None:
                ax.scatter(*zip(*sat[vnames].to_numpy()), color = self.cmap(norm(sat[self.hmv])), alpha = self.alpha_points)
            else:
                if self.gray_scale:
                    ax.scatter(*zip(*sat[vnames].to_numpy()), color = self.satcolor, marker = self.satmarker,  alpha = 1, label = 'Satisfied')
                else:
                    ax.scatter(*zip(*sat[vnames].to_numpy()), color = self.satcolor, marker = self.satmarker,  alpha = self.alpha_points, label = 'Satisfied')
        if self.hide_vio == False:
            if self.hmv != None:
                ax.scatter(*zip(*vio[vnames].to_numpy()), color = self.cmap(norm(vio[self.hmv])), alpha = self.alpha_points)
            else:
                if self.gray_scale:
                    ax.scatter(*zip(*vio[vnames].to_numpy()), color = self.viocolor, marker = self.viomarker, alpha = 1, facecolors = 'none', edgecolors = self.viocolor , label = 'Violated')
                else:
                    ax.scatter(*zip(*vio[vnames].to_numpy()), color = self.viocolor, marker = self.viomarker, alpha = self.alpha_points, label = 'Violated')
        if self.hide_surf == False:
            surf = ax.plot_trisurf(*zip(*vert), triangles = tri, color = self.surfcolor, alpha = self.alpha_surface, label = 'Design space')
            surf._facecolors2d=surf._facecolor3d
            surf._edgecolors2d=surf._edgecolor3d
        
        plt.xlabel(xlabe)
        plt.ylabel(ylabe)
        if self.leg:
            if len(ax.get_legend_handles_labels()[0]) == 0:
                pass
            else:
                plt.legend(loc = 'upper right')
        ax.set_zlabel(zlabe)

        if self.plot_ubd == None:
            pass
        else:    
            ax.set_xlim((self.plot_lbd[0], self.plot_ubd[0]))
            ax.set_ylim((self.plot_lbd[1], self.plot_ubd[1]))
            ax.set_zlim((self.plot_lbd[2], self.plot_ubd[2]))

        rdes = {'vol': vol, 'shp': shp, 'hmv_max': hmv_max, 'hmv_maxp': hmv_maxp, 
                'hmv_min': hmv_min, 'hmv_minp': hmv_minp, 'hmv_ave': hmv_ave, 'sat': sat, 'vio': vio}
        self.ax = ax
        self.rdes = rdes
        return rdes, ax

    def flex_cube(self, x, **kwargs):
        """
        Plot the flexibility cube
        """
        import numpy as np
        import matplotlib.pyplot as plt

        self.all_x.append(x)
        suppress_legend = kwargs.get('suppress_legend', False)
        
        # ----- External definitions ----- #
        sat = self.sat
        labels = self.labels
        units  = labels.get('units',  ['[-]', '[-]', '[-]'])
        vnames = labels.get('vnames', ['x', 'y', 'z'])
        nspace = max([len(i) for i in vnames])
        uspace = max([len(i) for i in units])
        
        # ----- Unpacking options ----- #
        options = kwargs.get('options', None)
        if options == None:
            ax = self.ax
        else:
            self.update_options(options)
            rdes, ax = self.plot()
        
        rcube = {}
        # ----- Creating design cube ----- #
        inputs_max = self.df[labels['vnames']].max().to_numpy()
        inputs_min = self.df[labels['vnames']].min().to_numpy()
        inputs_range = inputs_max - inputs_min
        pc = self.step_change/100
        flag = False
        while flag == False:
            cube_vert = np.array([[x[0] - pc*inputs_range[0], x[1] - pc*inputs_range[1], x[2] - pc*inputs_range[2]],
                                  [x[0] + pc*inputs_range[0], x[1] - pc*inputs_range[1], x[2] - pc*inputs_range[2]],
                                  [x[0] - pc*inputs_range[0], x[1] + pc*inputs_range[1], x[2] - pc*inputs_range[2]],
                                  [x[0] - pc*inputs_range[0], x[1] - pc*inputs_range[1], x[2] + pc*inputs_range[2]],
                                  [x[0] + pc*inputs_range[0], x[1] + pc*inputs_range[1], x[2] - pc*inputs_range[2]],
                                  [x[0] + pc*inputs_range[0], x[1] + pc*inputs_range[1], x[2] + pc*inputs_range[2]],
                                  [x[0] + pc*inputs_range[0], x[1] - pc*inputs_range[1], x[2] + pc*inputs_range[2]],
                                  [x[0] - pc*inputs_range[0], x[1] + pc*inputs_range[1], x[2] + pc*inputs_range[2]]])
            flag = False in [self.inShape(cube_vert[i]) for i in range(cube_vert.shape[0])]
            pc += self.step_change/100

        rmax = cube_vert.max(axis = 0)
        rmin = cube_vert.min(axis = 0)
        # ax.scatter(*zip(*cube_vert), marker = tmark, color = tcolor, s = 1)
        # print(rmax)
        # print(rmin)

        pc = (self.step_change/100)/100
        flag = True
        while flag == True:
            nvert = [[cube_vert[0, 0] + pc*inputs_range[0], cube_vert[0, 1] + pc*inputs_range[1], cube_vert[0, 2] + pc*inputs_range[2]],
                     [cube_vert[1, 0] - pc*inputs_range[0], cube_vert[1, 1] + pc*inputs_range[1], cube_vert[1, 2] + pc*inputs_range[2]],
                     [cube_vert[2, 0] + pc*inputs_range[0], cube_vert[2, 1] - pc*inputs_range[1], cube_vert[2, 2] + pc*inputs_range[2]],
                     [cube_vert[3, 0] + pc*inputs_range[0], cube_vert[3, 1] + pc*inputs_range[1], cube_vert[3, 2] - pc*inputs_range[2]],
                     [cube_vert[4, 0] - pc*inputs_range[0], cube_vert[4, 1] - pc*inputs_range[1], cube_vert[4, 2] + pc*inputs_range[2]],
                     [cube_vert[5, 0] - pc*inputs_range[0], cube_vert[5, 1] - pc*inputs_range[1], cube_vert[5, 2] - pc*inputs_range[2]],
                     [cube_vert[6, 0] - pc*inputs_range[0], cube_vert[6, 1] + pc*inputs_range[1], cube_vert[6, 2] - pc*inputs_range[2]],
                     [cube_vert[7, 0] + pc*inputs_range[0], cube_vert[7, 1] - pc*inputs_range[1], cube_vert[7, 2] - pc*inputs_range[2]]]
            nvert = np.array(nvert)
            flag = False in [self.inShape(nvert[i]) for i in range(nvert.shape[0])]
            pc += (self.step_change/100)/100

        rmax = nvert.max(axis = 0)
        rmin = nvert.min(axis = 0)

        ax.scatter(*zip(x), color = self.npcolor, s = self.msize, marker = self.npmarker, label = 'Nominal point')
        # ax.scatter(*zip(*nvert), marker = tmark, color = tcolor, s = msize)

        faces = [[nvert[0], nvert[1], nvert[4], nvert[2], nvert[0]],
                 [nvert[0], nvert[3], nvert[6], nvert[1], nvert[0]],
                 [nvert[3], nvert[7], nvert[5], nvert[6], nvert[3]], 
                 [nvert[6], nvert[1], nvert[4], nvert[5], nvert[6]],
                 [nvert[7], nvert[3], nvert[0], nvert[2], nvert[7]],
                 [nvert[2], nvert[4], nvert[5], nvert[7], nvert[2]]]
        for i in faces:
            plt.plot(*zip(*i[:-1]), color = self.ccolor, linewidth = self.clinewidth)
        plt.plot(*zip(*faces[-1]), color = self.ccolor, linewidth = self.clinewidth, label = 'Flexibility cube')
        cube_volume = (rmax - rmin).prod()
        plusmin = (rmax - rmin)/2
        print(f'Flexibility cube point: ')
        print(f'    {vnames[0]:{nspace}}: {x[0]:6.2f} ' + u'\u00B1 ' + f'{plusmin[0]:6.2f} {units[0]:{uspace}} Range: {rmin[0]:6.2f} - {rmax[0]:6.2f} {units[0]:{uspace}}')
        print(f'    {vnames[1]:{nspace}}: {x[1]:6.2f} ' + u'\u00B1 ' + f'{plusmin[1]:6.2f} {units[1]:{uspace}} Range: {rmin[1]:6.2f} - {rmax[1]:6.2f} {units[1]:{uspace}}')
        print(f'    {vnames[2]:{nspace}}: {x[2]:6.2f} ' + u'\u00B1 ' + f'{plusmin[2]:6.2f} {units[2]:{uspace}} Range: {rmin[2]:6.2f} - {rmax[2]:6.2f} {units[2]:{uspace}}')
        print(f'Flexibility cube volume: {cube_volume:.2f} {units[3]}')

        hmv_cube_flag = False

        if self.hmv != None:
            cube_df = sat.copy()
            for i in range(len(rmax)):
                cube_df = cube_df[cube_df[labels['vnames'][i]] <= rmax[i]]

            for i in range(len(rmin)):
                cube_df = cube_df[cube_df[labels['vnames'][i]] >= rmin[i]]
            if cube_df.shape[0] == 0:
                print('No samples inside flexibility cube available.')
                hmv_cube_flag = True

            # ----- Calculating Heatmapvar values ----- #
            if hmv_cube_flag == False:
                cube_no_sams  = cube_df.shape[0]
                cube_all_samples = cube_df.to_string()
                hmv_cube_ave  = cube_df[self.hmv].mean()
                hmv_cube_max  = cube_df[self.hmv].max()
                hmv_cube_maxp = cube_df[cube_df[self.hmv] == hmv_cube_max].to_string()
                hmv_cube_min  = cube_df[self.hmv].min()
                hmv_cube_minp = cube_df[cube_df[self.hmv] == hmv_cube_min].to_string()
            else:
                cube_no_sams     = None
                cube_all_samples = None
                hmv_cube_ave  = None
                hmv_cube_max  = None
                hmv_cube_maxp = None
                hmv_cube_min  = None
                hmv_cube_minp = None
        else:
            cube_no_sams     = None
            cube_all_samples = None
            hmv_cube_ave  = None
            hmv_cube_max  = None
            hmv_cube_maxp = None
            hmv_cube_min  = None
            hmv_cube_minp = None


        rcube = {'rmax': rmax, 'rmin': rmin, 'cube_volume': cube_volume, 'plusmin': plusmin, 
                 'cube_no_sams': cube_no_sams, 'hmv_cube_flag': hmv_cube_flag, 
                 'hmv_cube_max': hmv_cube_max, 'hmv_cube_maxp': hmv_cube_maxp,
                 'hmv_cube_min': hmv_cube_min, 'hmv_cube_minp': hmv_cube_minp, 
                 'hmv_cube_ave': hmv_cube_ave, 'cube_all_samples': cube_all_samples}
        self.all_fcube.append(rcube)
        
        if suppress_legend:
            pass
        else:
            if self.leg:
                if len(ax.get_legend_handles_labels()[0]) == 0:
                    pass
                else:
                    plt.legend(loc = 'upper right')
        
        return rcube, ax
        
    def savefig(self, fname = 'test.jpg', sdpi = 420):
        """
        Save figure
        """
        import matplotlib.pyplot as plt

        plt.savefig(fname, dpi = sdpi)
        
    def collect_frames(self, ax, anielev, sfolder, sname, sdpi = 100):
        """
        Collect .png images for animation of plot by rotating the 3D plot
        720 images will be collected with 0.5 increments for a total of 1 whole rotation
        Args:
            ax ([type]): matplotlib axes
            anielev ([type]): elevation of the figure
            sfolder ([type]): string of the save folder
            sname ([type]): save name of the pictures generated, will be followed by {i:04}.png
            sdpi (int, optional): [saved picture dpi]. Defaults to 100.
        """
        import matplotlib.pyplot as plt
        # Create save folder
        import os
        try:
            os.makedirs(sfolder)
        except FileExistsError:
            print('Folder already exist')
            
        ax.view_init(elev = anielev, azim = 0)
        for ii in range(0, 2*360, 1):
                ax.azim += 0.5
                plt.savefig(f'{sfolder}{sname}_frame_{ii:04}.png', dpi = sdpi)
                
    def send_output(self, sfolder = 'tmp/', output_filename = 'DSI_output', appendix = True):
        
        import os
        try:
            os.makedirs(sfolder)
        except FileExistsError:
            print('Folder already exist')
    
        f = open(f'{sfolder}{output_filename}.txt', 'w')
        # Headers
        f.write('Design Space Identification 3D\n')
        f.write(f'Dataset name: {output_filename}\n\n')
        f.write(f'No of samples: {self.df.shape[0]}\n')
        if self.labels["time_label"][1] == -1:
            time_t = 'last'
        else:
            time_t = self.labels["time_label"][1]
        f.write(f'Design space at time - {self.labels["time_label"][0]}: {time_t}\n\n')

        f.write('Variables/parameters varied: \n')
        for i, name in enumerate(self.labels["vnames"]):
            f.write(f'{name:12} [{self.labels["units"][i]}]\n')

        f.write('\nConstraints used: \n')
        for i in self.constraints:
            f.write(f'{i:15} Lower bound: {self.constraints[i][1]:5}     Upper bound: {self.constraints[i][0]:5}\n')
            
        # DSI results
        f.write(f'\n# ------------------------------ RESULTS ------------------------------ #\n')
        f.write(f'Design space volume: {self.rdes["vol"]:.2f} {self.labels["units"][3]}\n\n')
        f.write(f'Average {self.hmv}:    {self.rdes["hmv_ave"]:.2f} {self.labels["units"][4]}\n')
        f.write(f'DS Maximum {self.hmv}: {self.rdes["hmv_max"]:.2f} {self.labels["units"][4]}\n')
        f.write(f'DS Minimum {self.hmv}: {self.rdes["hmv_min"]:.2f} {self.labels["units"][4]}\n')
        f.write(f'\n-------------------------------------------------------------------------\n')
        f.write(f'Detailed maximum point: \n')
        f.write(f'{self.rdes["hmv_maxp"]}\n\n')
        f.write(f'Detailed minimum point: \n')
        f.write(f'{self.rdes["hmv_minp"]}')
        f.write(f'\n-------------------------------------------------------------------------\n')
        
        if len(self.all_fcube) != 0:
            for i in range(len(self.all_fcube)):
                rcube = self.all_fcube[i]
                x = self.all_x[i]
                rmax = rcube['rmax']
                rmin = rcube['rmin']
                vnames = self.labels['vnames']
                units = self.labels['units']

                cube_volume = (rmax - rmin).prod()
                plusmin = (rmax - rmin)/2
                nspace = max([len(i) for i in self.labels['vnames']])
                uspace = max([len(i) for i in self.labels['units']])

                if x != None:
                    f.write(f'\n\n\n# ------------------------------ Flexibility Cube {i+1:03} ------------------------------ #\n')
                    f.write(f'Flexibility cube point: \n')
                    f.write(f'{vnames[0]:{nspace}}: {x[0]:6.2f} ' + u'\u00B1 ' + f'{plusmin[0]:6.2f} {units[0]:{uspace}} Range: {rmin[0]:6.2f} - {rmax[0]:6.2f} {units[0]:{uspace}}\n')
                    f.write(f'{vnames[1]:{nspace}}: {x[1]:6.2f} ' + u'\u00B1 ' + f'{plusmin[1]:6.2f} {units[1]:{uspace}} Range: {rmin[1]:6.2f} - {rmax[1]:6.2f} {units[1]:{uspace}}\n')
                    f.write(f'{vnames[2]:{nspace}}: {x[2]:6.2f} ' + u'\u00B1 ' + f'{plusmin[2]:6.2f} {units[2]:{uspace}} Range: {rmin[2]:6.2f} - {rmax[2]:6.2f} {units[2]:{uspace}}\n')
                    f.write(f'Flexibility cube volume: {cube_volume:.2f} {units[3]}\n')
                    if rcube['hmv_cube_flag']:
                        f.write('No samples inside flexibility cube available.')
                    else:
                        f.write(f'\nNumber of samples inside flexibility cube: {rcube["cube_no_sams"]}\n')
                        f.write(f'Average {self.hmv}:    {rcube["hmv_cube_ave"]:.2f} {units[4]}\n')
                        f.write(f'DS Maximum {self.hmv}: {rcube["hmv_cube_max"]:.2f} {units[4]}\n')
                        f.write(f'DS Minimum {self.hmv}: {rcube["hmv_cube_min"]:.2f} {units[4]}\n')
                        f.write(f'\n-------------------------------------------------------------------------\n')
                        f.write(f'Detailed maximum point: \n')
                        f.write(f'{rcube["hmv_cube_maxp"]}\n\n')
                        f.write(f'Detailed minimum point: \n')
                        f.write(f'{rcube["hmv_cube_minp"]}\n')
                        f.write(f'\nAll samples inside flexibility cube: \n')
                        f.write(f'{rcube["cube_all_samples"]}')
                        f.write(f'\n-------------------------------------------------------------------------\n')
        
        if appendix:
            f.write('\n\n\n\n# ------------------------------ APPENDIX ------------------------------ #\n')
            f.write(f'ALL SATISFIED SAMPLES: \n')
            f.write(f'\n{self.rdes["sat"].to_string()}\n\n')
            f.write(f'\n-------------------------------------------------------------------------\n')
            f.write(f'ALL VIOLATED SAMPLES: \n')
            f.write(f'\n{self.rdes["vio"].to_string()}\n\n')
        
        f.close()
        