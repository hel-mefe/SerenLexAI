import { FormInput } from "./FormInput"
import { PasswordInput } from './PasswordInput'
import { PrimaryButton } from "./PrimaryButton"
import { AuthDivider } from "./AuthDivider"

export function SignInForm() {
  return (
    <div className="flex-1 flex items-center justify-center px-10 pb-6">
      <div className="w-full max-w-[340px]">
        <h2 className="text-3xl font-bold text-neutral-900 mb-1">
          Sign In
        </h2>

        <FormInput label="Email or Username" />
        <PasswordInput />

        <PrimaryButton>Sign In</PrimaryButton>

        <AuthDivider />

      </div>
    </div>
  )
}