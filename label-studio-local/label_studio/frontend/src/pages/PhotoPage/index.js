
import React from 'react';
import { SidebarMenu } from '../../components/SidebarMenu/SidebarMenu';
import { Photo } from './Photo';

const MenuLayout = ({ children, ...routeProps }) => {
  let menuItems = [Photo];

  return (
    <SidebarMenu
      menuItems={menuItems}
      path={routeProps.match.url}
      children={children}
    />
  );
};

const photoPages = {};

export const PhotoPage = {
  title: "Photo",
  path: "/photo",
  exact: true,
  layout: MenuLayout,
  component: Photo,
  pages: photoPages,
};
