import React from 'react';
import GenericServiceApplication from './GenericServiceApplication';
export const PropertyRegistrationApplication: React.FC = () => <GenericServiceApplication serviceId="property_registration" title="Property Registration" description="Register a property transaction and prepare the ownership record workflow." defaultCustomerType="citizen" />;
export default PropertyRegistrationApplication;
