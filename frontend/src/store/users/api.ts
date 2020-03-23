import { client } from '@/store/api'

import { User } from '@/@types/users';

export async function checkEmailExists(email: string): Promise<{ email: string }> {
  const response = await client.get(`users/${email}/exists/`)
  return response.data
}

export async function getCurrentUser(): Promise<User> {
  const response = await client.get(`users/current/`)
  return response.data
}

export async function getMagicLink(id: string): Promise<{email: string, token: string}> {
  const response  = await client.get(`users/magic_link/${id}/`)
  return response.data
}

export async function updateUserPassword(password: string): Promise<User> {
  const response = await client.put(`users/current/set_password/`, { password })
  return response.data
}

export async function login(user: string, password: string): Promise<{ id: string, token: string }> {
  const response = await client.post(`users/login/`, { user, password })
  return response.data
}

export async function forgotPassword(email: string): Promise<{ email: string }> {
  const response = await client.post(`users/forgot_password/`, { email })
  return response.data
}

export async function getResetPasswordLink(id: string): Promise<{ id: string, email: string }> {
  const response = await client.get(`users/reset_password/${id}/`)
  return response.data
}

export async function resetPassword(id: string, password: string): Promise<{ id: string, email: string }> {
  const response = await client.put(`users/reset_password/${id}/`, { password })
  return response.data
}