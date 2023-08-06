import React from 'react'
import {Box, EntityList, Typography} from 'system/components'
import {ScreenProps} from 'system/screens'
import {gettext} from 'system/l10n'
import {runtime} from 'system/project'
import {api} from 'system/api'
import {RequestApiPath} from 'system/routing'


const itemScreenPath: string = '/settings/system/roles/{key}'
const addScreenPath: string = '/settings/system/roles/new'
const objectsPath: RequestApiPath = api.entityPath('system', 'Role')


export default class Screen extends React.Component<ScreenProps> {
  restoreScrollPosition = (): void => {
    runtime.restoreScrollPosition()
  }

  render() {
    return (
      <Box mt={1}>
        <Typography variant={'h4'} paddingBottom={2}>
          {gettext("Administrate roles", 'system.aaa')}
        </Typography>
        <EntityList
          addScreenPath={addScreenPath}
          defaultSort={{value: 'name', direction: 'asc'}}
          deleteAction={true}
          entityCaption={gettext("Roles list", 'system.aaa')}
          itemsRoute={itemScreenPath}
          limit={25}
          pagination
          primaryField={'name'}
          requestPath={objectsPath}
          search
          selectable
          textTotalCount
          urlStateOffset
          urlStateSearch
          onFetchDone={this.restoreScrollPosition}
        />
      </Box>
    )
  }
}
