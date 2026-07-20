import re, json, os

RAW = {}

RAW["4269153"] = r"""
ID: 4269153
Name: Northstone Realty
Stage: Onboarding In Progress
Owner: Shweta Gouda (ID: 73360)
Created At: 2026-05-15T13:04:45.507Z
Custom fields:
  cfPlanType: {'id': 186117, 'name': 'Broker'}
  cfReDeveloperOrChannelPartner: {'id': 186098, 'name': 'Broker'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-05-18T18:30:00.000Z
  cfCity: Ambernath
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfOwnerPhoneNumber: +919999977777
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  noOfLicenses: 6
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfCustomerCategory: {'id': 186493, 'name': 'Broker'}
  cfAdminTrainingStatus: {'id': 136872, 'name': 'Waiting on customer'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136746, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfPaymentCycle: {'id': 136719, 'name': 'Yearly'}
  cfSaleClosedBy: {'id': 175570, 'name': 'Alok Tiwari'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-06-28T18:30:00.000Z
"""

RAW["4255693"] = r"""
ID: 4255693
Name: Calicut Landmark Builders Pvt. Ltd
Stage: Pending on Customer
Owner: Raahul Ramanan R (ID: 71239)
Created At: 2026-05-13T08:19:04.334Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136829, 'name': 'Completed'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 36
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136780, 'name': 'Waiting on customer'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-20T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136837, 'name': 'Completed'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-05-12T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136883, 'name': 'Signed up'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfBilledAmount: 627760
  cfCostSheetTemplateSetupStatus: {'id': 136776, 'name': 'Waiting on customer'}
  cfSiteVisitFormSetupStatus: {'id': 136787, 'name': 'Initiated'}
  cfInventorySetup: {'id': 136731, 'name': 'Initiated'}
  cfWhatsappIntegrationStatus: {'id': 136852, 'name': 'Waiting on customer'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 308560
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfMarketingTrainingStatus: {'id': 136876, 'name': 'Waiting on customer'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136743, 'name': 'Initiated'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136849, 'name': 'Completed'}
  cfActualGoLiveDate: 2026-07-20T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136824, 'name': 'Waiting on customer'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136872, 'name': 'Waiting on customer'}
"""

RAW["4255681"] = r"""
ID: 4255681
Name: SPR Construction Pvt Ltd
Stage: Onboarding In Progress
Owner: Raahul Ramanan R (ID: 71239)
Created At: 2026-05-13T08:15:40.069Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136827, 'name': 'Initiated'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 41
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136820, 'name': 'Waiting on customer'}
  cfTargetGoLiveDate: 2026-05-30T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136837, 'name': 'Completed'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-05-10T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 14660
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136787, 'name': 'Initiated'}
  cfInventorySetup: {'id': 136731, 'name': 'Initiated'}
  cfWhatsappIntegrationStatus: {'id': 136852, 'name': 'Waiting on customer'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 637000
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfMarketingTrainingStatus: {'id': 136876, 'name': 'Waiting on customer'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136743, 'name': 'Initiated'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfActualGoLiveDate: 2026-07-06T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136824, 'name': 'Waiting on customer'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136872, 'name': 'Waiting on customer'}
"""

RAW["4241966"] = r"""
ID: 4241966
Name: GGC AI Calling
Stage: Pending on Customer
Owner: Venkat Viswavardhan (ID: 71242)
Created At: 2026-05-09T08:34:23.975Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136830, 'name': 'Not required'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 2
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-16T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-04-12T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136854, 'name': 'Not required'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 825999
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136742, 'name': 'Not required'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136870, 'name': 'Not required'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136826, 'name': 'Not required'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136874, 'name': 'Not required'}
"""

RAW["4233760"] = r"""
ID: 4233760
Name: Mythri Builder AI Calling
Stage: Pending on Customer
Owner: Venkat Viswavardhan (ID: 71242)
Created At: 2026-05-07T05:39:43.581Z
Custom fields:
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136742, 'name': 'Not required'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 2
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136744, 'name': 'Waiting on customer'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-16T18:30:00.000Z
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-04-22T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfSalesTrainingStatus: {'id': 136870, 'name': 'Not required'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfAdminTrainingStatus: {'id': 136874, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 354000
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
"""

RAW["4233715"] = r"""
ID: 4233715
Name: Kohinoor AI Calling
Stage: Pending on Customer
Owner: Venkat Viswavardhan (ID: 71242)
Created At: 2026-05-07T05:31:03.120Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136830, 'name': 'Not required'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 2
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-16T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-04-21T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136854, 'name': 'Not required'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136742, 'name': 'Not required'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136745, 'name': 'Completed'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136870, 'name': 'Not required'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136826, 'name': 'Not required'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136874, 'name': 'Not required'}
"""

RAW["4230613"] = r"""
ID: 4230613
Name: Kunwarji Realtors
Stage: Onboarding In Progress
Owner: Sanket Nampalliwar (ID: 71241)
Created At: 2026-05-06T07:50:41.554Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136829, 'name': 'Completed'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136808, 'name': 'Waiting on customer'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 150
  cfPropertyPortalIntegrationStatus: {'id': 136845, 'name': 'Completed'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-05-21T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136837, 'name': 'Completed'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-05-03T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136861, 'name': 'Completed'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136812, 'name': 'Waiting on customer'}
  cfBilledAmount: 1428980
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136853, 'name': 'Completed'}
  cfGoalsSetupStatus: {'id': 136764, 'name': 'Waiting on customer'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 861881
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136757, 'name': 'Completed'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfMarketingTrainingStatus: {'id': 136877, 'name': 'Completed'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136761, 'name': 'Completed'}
  cfOwnerDashboardSetupStatus: {'id': 136753, 'name': 'Completed'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136745, 'name': 'Completed'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136857, 'name': 'Completed'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfActualGoLiveDate: 2026-05-21T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136825, 'name': 'Completed'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136872, 'name': 'Waiting on customer'}
"""

RAW["4177642"] = r"""
ID: 4177642
Name: NPS DEVELOPERS
Stage: Onboarding In Progress
Owner: Raahul Ramanan R (ID: 71239)
Created At: 2026-04-27T04:20:35.549Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136828, 'name': 'Waiting on customer'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 11
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-20T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-04-26T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136811, 'name': 'Initiated'}
  cfBilledAmount: 428104
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136851, 'name': 'Initiated'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 428104
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136755, 'name': 'Initiated'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfPostSalesTemplatesSetup: {'id': 136894, 'name': 'Initiated'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136743, 'name': 'Initiated'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136867, 'name': 'Initiated'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfActualGoLiveDate: 2026-07-20T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136823, 'name': 'Initiated'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136871, 'name': 'Initiated'}
"""

RAW["3968505"] = r"""
ID: 3968505
Name: GRUHAM SPACES LLP
Stage: Onboarding In Progress
Owner: Venkat Viswavardhan (ID: 71242)
Created At: 2026-03-16T05:40:38.936Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136830, 'name': 'Not required'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 40
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-14T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-03-15T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136861, 'name': 'Completed'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 481440
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136789, 'name': 'Completed'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136854, 'name': 'Not required'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 440640
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136757, 'name': 'Completed'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136742, 'name': 'Not required'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136753, 'name': 'Completed'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136746, 'name': 'Not required'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfActualGoLiveDate: 2026-05-05T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136773, 'name': 'Completed'}
  cfWhatsappTemplateSetupStatus: {'id': 136826, 'name': 'Not required'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136873, 'name': 'Completed'}
"""

RAW["3575524"] = r"""
ID: 3575524
Name: Voora Developers
Stage: Pending on Customer
Owner: Raahul Ramanan R (ID: 71239)
Created At: 2026-01-12T12:52:39.883Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136829, 'name': 'Completed'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 21
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136781, 'name': 'Completed'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-09T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136837, 'name': 'Completed'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-01-11T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136861, 'name': 'Completed'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136811, 'name': 'Initiated'}
  cfBilledAmount: 785880
  cfCostSheetTemplateSetupStatus: {'id': 136777, 'name': 'Completed'}
  cfSiteVisitFormSetupStatus: {'id': 136789, 'name': 'Completed'}
  cfInventorySetup: {'id': 136733, 'name': 'Completed'}
  cfWhatsappIntegrationStatus: {'id': 136853, 'name': 'Completed'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136749, 'name': 'Completed'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 785880
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136757, 'name': 'Completed'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfMarketingTrainingStatus: {'id': 136877, 'name': 'Completed'}
  cfBookingDocumentsSetupStatus: {'id': 136785, 'name': 'Completed'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136799, 'name': 'Initiated'}
  cfCloudTelephonySetup: {'id': 136745, 'name': 'Completed'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136849, 'name': 'Completed'}
  cfActualGoLiveDate: 2026-07-09T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136825, 'name': 'Completed'}
  cfBulkDialerSetupStatus: {'id': 136793, 'name': 'Completed'}
  cfAdminTrainingStatus: {'id': 136873, 'name': 'Completed'}
"""

RAW["3304063"] = r"""
ID: 3304063
Name: Shree Honda
Stage: Onboarding In Progress
Owner: Sourabh Sahu (ID: 83260)
Created At: 2025-09-30T07:19:12.625Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136830, 'name': 'Not required'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 5
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-30T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2025-07-17T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 210984
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136852, 'name': 'Waiting on customer'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 210985
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136739, 'name': 'Initiated'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136743, 'name': 'Initiated'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136867, 'name': 'Initiated'}
  cfWorkflowAutomationSetupStatus: {'id': 136856, 'name': 'Waiting on customer'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136824, 'name': 'Waiting on customer'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136871, 'name': 'Initiated'}
"""

RAW["3304062"] = r"""
ID: 3304062
Name: Shree Automotive
Stage: Onboarding In Progress
Owner: Sourabh Sahu (ID: 83260)
Created At: 2025-09-30T07:19:12.399Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136830, 'name': 'Not required'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 4
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-30T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2025-07-17T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 104784
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136852, 'name': 'Waiting on customer'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 104783
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136739, 'name': 'Initiated'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136743, 'name': 'Initiated'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136867, 'name': 'Initiated'}
  cfWorkflowAutomationSetupStatus: {'id': 136856, 'name': 'Waiting on customer'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136824, 'name': 'Waiting on customer'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136871, 'name': 'Initiated'}
"""

RAW["3302998"] = r"""
ID: 3302998
Name: Times Group
Stage: Pending on Customer
Owner: Sanket Nampalliwar (ID: 71241)
Created At: 2025-09-29T13:18:02.011Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136830, 'name': 'Not required'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 50
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136822, 'name': 'Not required'}
  cfTargetGoLiveDate: 2026-07-23T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2025-06-23T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136834, 'name': 'Not required'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136738, 'name': 'Not required'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 944000
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136733, 'name': 'Completed'}
  cfWhatsappIntegrationStatus: {'id': 136854, 'name': 'Not required'}
  cfGoalsSetupStatus: {'id': 136766, 'name': 'Not required'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 944000
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136742, 'name': 'Not required'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136753, 'name': 'Completed'}
  cfErpIntegrationStatus: {'id': 136802, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136746, 'name': 'Not required'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136867, 'name': 'Initiated'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfOnboardingFeedbackReceived: {'id': 175589, 'name': 'No'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136826, 'name': 'Not required'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136871, 'name': 'Initiated'}
"""

RAW["4144089"] = r"""
ID: 4144089
Name: Dhanraj Realbuild Llp
Stage: Pending on Customer
Owner: Venkat Viswavardhan (ID: 71242)
Created At: 2026-04-22T07:27:29.948Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136829, 'name': 'Completed'}
  cfBookingsImport: {'id': 136893, 'name': 'Not required'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 6
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-16T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-04-21T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136861, 'name': 'Completed'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 538552
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136790, 'name': 'Not required'}
  cfInventorySetup: {'id': 136734, 'name': 'Not required'}
  cfWhatsappIntegrationStatus: {'id': 136853, 'name': 'Completed'}
  cfGoalsSetupStatus: {'id': 136765, 'name': 'Completed'}
  cfLinkedinLeadsIntegrationStatus: {'id': 136842, 'name': 'Not required'}
  cfCustomerCategory: {'id': 136715, 'name': 'C'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 538552
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136757, 'name': 'Completed'}
  cfApprovalSetupStatus: {'id': 136798, 'name': 'Not required'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfMarketingTrainingStatus: {'id': 136878, 'name': 'Not required'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136753, 'name': 'Completed'}
  cfCloudTelephonySetup: {'id': 136746, 'name': 'Not required'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136857, 'name': 'Completed'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfActualGoLiveDate: 2026-04-23T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136774, 'name': 'Not required'}
  cfWhatsappTemplateSetupStatus: {'id': 136825, 'name': 'Completed'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136873, 'name': 'Completed'}
"""

RAW["4147287"] = r"""
ID: 4147287
Name: Dreamworks Realtors
Stage: Pending on Customer
Owner: Venkat Viswavardhan (ID: 71242)
Created At: 2026-04-22T12:51:30.041Z
Custom fields:
  cfWebsiteIntegrationStatus: {'id': 136829, 'name': 'Completed'}
  cfRoiConfigurationSetupStatus: {'id': 136810, 'name': 'Not required'}
  cfZohoAnalyticsSetupStatus: {'id': 136770, 'name': 'Not required'}
  noOfLicenses: 21
  cfPropertyPortalIntegrationStatus: {'id': 136846, 'name': 'Not required'}
  cfPaymentScheduleTemplateSetupStatus: {'id': 136782, 'name': 'Not required'}
  cfPipelineSetupStatus: {'id': 136821, 'name': 'Completed'}
  cfTargetGoLiveDate: 2026-07-16T18:30:00.000Z
  cfGoogleLeadsIntegrationStatus: {'id': 136838, 'name': 'Not required'}
  cfHandoverStatus: {'id': 136887, 'name': 'Pending with OB'}
  cfActualStartDate: 2026-04-21T18:30:00.000Z
  cfFacebookLeadgenIntegrationStatus: {'id': 136833, 'name': 'Completed'}
  cfAccountActivationStatus: {'id': 136884, 'name': 'Active'}
  cfOfflineTrackerAppSetup: {'id': 136862, 'name': 'Not required'}
  cfRoutingSetup: {'id': 136737, 'name': 'Completed'}
  cfSmsTemplateSetupStatus: {'id': 136814, 'name': 'Not required'}
  cfBilledAmount: 642628
  cfCostSheetTemplateSetupStatus: {'id': 136778, 'name': 'Not required'}
  cfSiteVisitFormSetupStatus: {'id': 136789, 'name': 'Completed'}
  cfInventorySetup: {'id': 136733, 'name': 'Completed'}
  cfWhatsappIntegrationStatus: {'id': 136853, 'name': 'Completed'}
  cfGoalsSetupStatus: {'id': 136765, 'name': 'Completed'}
  cfCustomerCategory: {'id': 136713, 'name': 'A'}
  cfDltSetup: {'id': 136750, 'name': 'Not required'}
  cfProjectsSetup: {'id': 136724, 'name': 'Completed'}
  cfActualPaymentReceived: 642628
  cfOnlineMeetingIntegration: {'id': 136866, 'name': 'Not required'}
  cfSalesDashboardSetupStatus: {'id': 136758, 'name': 'Not required'}
  cfApprovalSetupStatus: {'id': 136797, 'name': 'Completed'}
  cfLeadImport: {'id': 136741, 'name': 'Completed'}
  cfMarketingTrainingStatus: {'id': 136877, 'name': 'Completed'}
  cfBookingDocumentsSetupStatus: {'id': 136786, 'name': 'Not required'}
  cfUsersSetup: {'id': 136729, 'name': 'Completed'}
  cfMarketingDashboardSetupStatus: {'id': 136762, 'name': 'Not required'}
  cfOwnerDashboardSetupStatus: {'id': 136754, 'name': 'Not required'}
  cfCloudTelephonySetup: {'id': 136745, 'name': 'Completed'}
  cfReDeveloperOrChannelPartner: {'id': 81825, 'name': 'Developer'}
  cfSalesTrainingStatus: {'id': 136869, 'name': 'Completed'}
  cfWorkflowAutomationSetupStatus: {'id': 136858, 'name': 'Not required'}
  cfEmailSubdomainSetup: {'id': 136850, 'name': 'Not required'}
  cfActualGoLiveDate: 2026-06-17T18:30:00.000Z
  cfChannelPartnerSetupStatus: {'id': 136773, 'name': 'Completed'}
  cfWhatsappTemplateSetupStatus: {'id': 136824, 'name': 'Waiting on customer'}
  cfBulkDialerSetupStatus: {'id': 136794, 'name': 'Not required'}
  cfAdminTrainingStatus: {'id': 136873, 'name': 'Completed'}
"""

STATUS_MAP = {
    "usersSetup":"cfUsersSetup","projectsSetup":"cfProjectsSetup","routingSetup":"cfRoutingSetup",
    "pipelineSetup":"cfPipelineSetupStatus","leadImport":"cfLeadImport","website":"cfWebsiteIntegrationStatus",
    "facebook":"cfFacebookLeadgenIntegrationStatus","propertyPortal":"cfPropertyPortalIntegrationStatus",
    "google":"cfGoogleLeadsIntegrationStatus","linkedin":"cfLinkedinLeadsIntegrationStatus",
    "whatsapp":"cfWhatsappIntegrationStatus","whatsappTemplate":"cfWhatsappTemplateSetupStatus",
    "cloudTelephony":"cfCloudTelephonySetup","dlt":"cfDltSetup","offlineTracker":"cfOfflineTrackerAppSetup",
    "inventorySetup":"cfInventorySetup","siteVisitForm":"cfSiteVisitFormSetupStatus",
    "channelPartner":"cfChannelPartnerSetupStatus","workflow":"cfWorkflowAutomationSetupStatus",
    "salesTraining":"cfSalesTrainingStatus","adminTraining":"cfAdminTrainingStatus",
    "marketingTraining":"cfMarketingTrainingStatus","costSheet":"cfCostSheetTemplateSetupStatus",
    "paymentSchedule":"cfPaymentScheduleTemplateSetupStatus","bookingDocs":"cfBookingDocumentsSetupStatus",
    "bookingsImport":"cfBookingsImport","postSalesTemplates":"cfPostSalesTemplatesSetup",
    "salesDashboard":"cfSalesDashboardSetupStatus","ownerDashboard":"cfOwnerDashboardSetupStatus",
    "marketingDashboard":"cfMarketingDashboardSetupStatus","goals":"cfGoalsSetupStatus",
    "roi":"cfRoiConfigurationSetupStatus","bulkDialer":"cfBulkDialerSetupStatus",
    "emailSubdomain":"cfEmailSubdomainSetup","erp":"cfErpIntegrationStatus",
    "zohoAnalytics":"cfZohoAnalyticsSetupStatus","approval":"cfApprovalSetupStatus",
    "onlineMeeting":"cfOnlineMeetingIntegration",
}

def code(name):
    if name is None:
        return "-"
    if "Complet" in name:
        return "C"
    if "Initiat" in name:
        return "I"
    if name == "Not required":
        return "N"
    if ("Waiting" in name) or ("Change requested" in name) or ("customize" in name) or ("Engineering" in name):
        return "W"
    return "-"  # fallback (shouldn't happen)

def parse(raw):
    hdr = {}
    for key in ["ID","Name","Stage"]:
        m = re.search(r"^%s: (.*)$" % key, raw, re.M)
        hdr[key] = m.group(1).strip() if m else None
    m = re.search(r"^Owner: (.*?)(?: \(ID: \d+\))?$", raw, re.M)
    hdr["Owner"] = m.group(1).strip() if m else None
    m = re.search(r"^Created At: (.*)$", raw, re.M)
    hdr["Created"] = m.group(1).strip() if m else None
    cf = {}
    for line in raw.splitlines():
        m = re.match(r"^  (cf\w+|noOfLicenses): (.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        nm = re.search(r"'name': '([^']*)'", v)
        if nm:
            cf[k] = nm.group(1)
        else:
            cf[k] = v
    return hdr, cf

def as_int(cf, k):
    if k in cf:
        try:
            return int(cf[k])
        except:
            return None
    return None

out = {}
for did, raw in RAW.items():
    hdr, cf = parse(raw)
    rec = {}
    rec["name"] = hdr["Name"]
    rec["owner"] = hdr["Owner"]
    rec["stage"] = hdr["Stage"]
    rec["created"] = hdr["Created"]
    for outk, cfk in STATUS_MAP.items():
        rec[outk] = code(cf.get(cfk)) if cfk in cf else "-"
    rec["activation"] = cf.get("cfAccountActivationStatus")
    rec["segment"] = cf.get("cfReDeveloperOrChannelPartner")
    rec["category"] = cf.get("cfCustomerCategory")
    rec["handover"] = cf.get("cfHandoverStatus")
    rec["feedback"] = cf.get("cfOnboardingFeedbackReceived")
    tools = cf.get("cfRequiredTools")
    if tools is None or tools == "None":
        rec["tools"] = []
    else:
        rec["tools"] = tools if isinstance(tools, list) else [tools]
    rec["licences"] = as_int(cf, "noOfLicenses")
    rec["billed"] = as_int(cf, "cfBilledAmount")
    rec["recv"] = as_int(cf, "cfActualPaymentReceived")
    rec["targetGoLive"] = cf["cfTargetGoLiveDate"][:10] if "cfTargetGoLiveDate" in cf else None
    rec["actualStart"] = cf["cfActualStartDate"][:10] if "cfActualStartDate" in cf else None
    rec["actualGoLive"] = cf["cfActualGoLiveDate"][:10] if "cfActualGoLiveDate" in cf else None
    out[did] = rec

order = ["4269153","4255693","4255681","4241966","4233760","4233715","4230613",
         "4177642","4147287","4144089","3968505","3575524","3304063","3304062","3302998"]
# 4147287 not in RAW yet? include
missing = [d for d in order if d not in out]
print("MISSING:", missing)
ordered = {d: out[d] for d in order if d in out}

os.makedirs("/sessions/eager-friendly-knuth/mnt/kylas-crm-mcp-server/onboarding_reports", exist_ok=True)
p = "/sessions/eager-friendly-knuth/mnt/kylas-crm-mcp-server/onboarding_reports/deal_fields_2026-07-16_d.json"
with open(p, "w") as f:
    json.dump(ordered, f, indent=2)
print("wrote", p, "deals:", len(ordered))
print("status keys per rec:", len(STATUS_MAP))
