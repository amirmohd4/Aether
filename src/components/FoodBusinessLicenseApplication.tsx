import React from 'react';
import GenericServiceApplication from './GenericServiceApplication';

export const FoodBusinessLicenseApplication: React.FC = () => (
  <GenericServiceApplication
    serviceId="food_business_license"
    title="Food Business License / Registration"
    description="Start an eligible food-business licensing or registration workflow and prepare the Aether case."
    defaultCustomerType="business"
  />
);

export default FoodBusinessLicenseApplication;
