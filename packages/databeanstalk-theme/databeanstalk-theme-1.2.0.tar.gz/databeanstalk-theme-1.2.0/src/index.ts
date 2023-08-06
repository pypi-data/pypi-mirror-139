import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @databeanstalk/databeanstalk-theme extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: '@databeanstalk/databeanstalk-theme',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension @databeanstalk/databeanstalk-theme is activated!');
    const style = '@databeanstalk/databeanstalk-theme/index.css';

    manager.register({
      name: 'DatabeanStalk UI Dark',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default extension;
