import { client } from '@/store/api'
import { TLCStepLicenseName } from '@/@types/quote'


export async function getTLCLicenseName(licenseNumber: string): Promise<TLCStepLicenseName> {
    const response = await client.get(`importer/active_driver/${licenseNumber}/`)
    return response.data
}