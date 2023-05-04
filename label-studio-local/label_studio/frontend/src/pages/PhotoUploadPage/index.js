
import React from 'react';
import { SidebarMenu } from '../../components/SidebarMenu/SidebarMenu';
import { PhotoUpload } from './PhotoUpload';

const MenuLayout = ({ children, ...routeProps }) => {
  let menuItems = [PhotoUpload];

  return (
    <SidebarMenu
      menuItems={menuItems}
      path={routeProps.match.url}
      children={children}
    />
  );
};

const photoUploadPages = {};

export const PhotoUploadPage = {
  title: "PhotoUpload",
  path: "/photo_upload",
  exact: true,
  layout: MenuLayout,
  component: PhotoUpload,
  pages: photoUploadPages,
};
