import { client } from '@/store/api'
import { TLCStepLicenseName, VINStepFHVInfo, VINStepInsuranceInfo } from '@/@types/quote'


export async function getTLCLicenseName(licenseNumber: string): Promise<TLCStepLicenseName> {
    const response = await client.get(`importer/fhv_driver/${licenseNumber}/`)
    return response.data
}

export async function getVINFHVInfo(vehicle_vin_number: string): Promise<VINStepFHVInfo> {
  const response = await client.get(`importer/for_hire_vehicle/${vehicle_vin_number}/`)
  return {
    ...response.data,
    vehicle_owner: response.data.name,
    license_plate: response.data.dmv_license_plate_number,
    vehicle_vin: response.data.vehicle_vin_number,
  }
}

export async function getVINInsuranceInfo(vin: string): Promise<VINStepInsuranceInfo> {
  const response = await client.get(`importer/vehicle_insurance_information/${vin}/`)
  return {
    insurance_carrier_name: response.data.automobile_insurance_name,
    insurance_policy_number: response.data.automobile_insurance_policy_number,
  }
}