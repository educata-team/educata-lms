import styles from '../styles.module.scss';
import React from 'react';
import { FC } from '../../../../common/types/react/fc.type';
import TreeView from '@mui/lab/TreeView';
import TreeItem from '@mui/lab/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { v4 as uuidv4 } from 'uuid';

interface Unit{
  unitName: string;
  lessonsName: Array<string>;
}

interface Props{
  navigation: Array<Unit>;
}

export const NavigationPanel:FC<Props> = ({
  navigation,
                                          }) => {

  const units = [];

  for (let i = 0; i < navigation.length; i++){
    const lessons = [];
    for(let j = 0; j < navigation[i].lessonsName.length; j++){
      lessons.push(
        <TreeItem label={navigation[i].lessonsName[j]} nodeId={uuidv4()}/>,
      );
    }

    units.push(
      <TreeItem label={`Unit ${i+1}. ${navigation[i].unitName}`} nodeId={uuidv4()}>
        {lessons}
      </TreeItem>,
    );
  }

  return (
    <div className={styles['navigation-panel']}>
      <h2>Course Information</h2>

      <TreeView
        aria-label="file system navigator"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        sx={{ flexGrow: 1, maxWidth: 200, overflowY: 'auto' }}
      >
        <TreeItem nodeId="1" label="Course Material">
          {units}
        </TreeItem>
      </TreeView>

    </div>
  );
};
