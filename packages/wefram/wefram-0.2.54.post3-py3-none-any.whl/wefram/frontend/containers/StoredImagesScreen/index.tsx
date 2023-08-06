import React from 'react'
import {ScreenProps} from 'system/screens'
import {
  Box,
  StoredImagesList,
  Typography
} from 'system/components'
import {runtime} from 'system/project'


type ScreenState = {
  loading: boolean
}


export default class Screen extends React.Component<ScreenProps, ScreenState> {
  state: ScreenState = {
    loading: true
  }

  render() {
    const screenCaption: string = runtime.screens[this.props.name].caption
    return (
      <React.Fragment>
        <Box mt={1}>
          <Typography variant={'h4'} paddingBottom={2}>{screenCaption || 'Images'}</Typography>
        </Box>
        <Box>
          <StoredImagesList
            apiEntity={this.props.params['apiEntity']}
            storageEntity={this.props.params['storageEntity']}
            columns={this.props.params.columns}
            minHeight={'calc(100vh - 72px)'}
            rowHeight={this.props.params.rowHeight}
            gap={this.props.params.gap}
          />
        </Box>
      </React.Fragment>
    )
  }
}
