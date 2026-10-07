import React from 'react';
import GenericServiceApplication from './GenericServiceApplication';

export const MedicalLicenseApplication: React.FC = () => (
  <GenericServiceApplication
    serviceId="medical_license"
    title="Medical License"
    description="Start an eligible medical-license or establishment workflow and prepare its Aether case."
    defaultCustomerType="business"
  />
);

export default MedicalLicenseApplication;
