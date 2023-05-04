
import React from 'react';
import { SidebarMenu } from '../../components/SidebarMenu/SidebarMenu';
import { PhotoDetect } from './PhotoDetect';

const MenuLayout = ({ children, ...routeProps }) => {
  let menuItems = [PhotoDetect];

  return (
    <SidebarMenu
      menuItems={menuItems}
      path={routeProps.match.url}
      children={children}
    />
  );
};

const photoDetectPages = {};

export const PhotoDetectPage = {
  title: "PhotoDetect",
  path: "/photo_detect",
  exact: true,
  layout: MenuLayout,
  component: PhotoDetect,
  pages: photoDetectPages,
};
