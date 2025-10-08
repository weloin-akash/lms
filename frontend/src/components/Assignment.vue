<template>
	<div
		v-if="assignment.data"
		class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 lg:h-screen h-full overflow-y-auto lg:overflow-hidden"
		:class="{ 'rounded-xl overflow-hidden shadow-lg border border-gray-200/50': !showTitle }"
	>
		<div class="flex flex-col lg:grid lg:grid-cols-2 gap-0 lg:h-full">
			<!-- Question Section with Modern Card Design -->
			<div
				class="bg-white/80 backdrop-blur-sm border-0 lg:border-r border-gray-200/50 overflow-y-auto"
				:class="{ 'h-full lg:h-[calc(100vh-3.2rem)] pr-2 py-8 pl-4': showTitle, 'lg:h-full p-8': !showTitle }"
			>
				<!-- Modern Header -->
				<div v-if="showTitle" class="mb-8">
					<div class="flex items-center space-x-3 mb-4">
						<div class="w-10 h-10 bg-[#ed8e22] rounded-xl flex items-center justify-center">
							<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
							</svg>
						</div>
						<div>
							<h2 class="text-xl font-bold text-gray-900">
								<span v-if="submissionName === 'new'">
									{{ __('Submission by') }} {{ user.data?.full_name }}
								</span>
								<span v-else>
									{{ __('Submission by') }} {{ submissionResource.doc?.member_name }}
								</span>
							</h2>
							<p class="text-gray-600 text-sm">Assignment Response</p>
						</div>
					</div>
				</div>

				<!-- Question Card -->
				<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-6">
					<div class="flex items-center space-x-2 mb-4">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<h3 class="text-lg font-semibold text-gray-900">{{ __('Assignment Question') }}</h3>
					</div>
					<div
						v-html="assignment.data.question"
						class="ProseMirror prose prose-table:table-fixed prose-td:p-3 prose-th:p-3 prose-td:border prose-th:border prose-td:border-gray-200 prose-th:border-gray-200 prose-td:relative prose-th:relative prose-th:bg-gray-50 prose-sm max-w-none !whitespace-normal text-gray-700 leading-relaxed"
					></div>
				</div>
			</div>

			<!-- Submission Section with Modern Design -->
			<div class="bg-white/80 backdrop-blur-sm p-4 sm:p-6 lg:pr-6 lg:pl-0 lg:py-8 space-y-6">
				<!-- Submission Header -->
				<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6">
					<div class="flex items-center justify-between mb-6">
						<div class="flex items-center space-x-3">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<h3 class="text-lg font-semibold text-gray-900">{{ __('Your Submission') }}</h3>
						</div>
						<div class="flex items-center gap-3">
							<div v-if="isDirty" class="flex items-center h-9 px-3 rounded-full text-sm font-medium bg-orange-100 text-orange-800 border border-orange-200">
								<div class="w-2 h-2 bg-orange-500 rounded-full mr-2 animate-pulse"></div>
								{{ __('Unsaved Changes') }}
							</div>
							<div
								v-else-if="submissionResource.doc?.status"
								class="flex items-center h-9 px-3 rounded-full text-sm font-medium border"
								:class="{
									'bg-green-100 text-green-800 border-green-200': statusTheme === 'green',
									'bg-blue-100 text-blue-800 border-blue-200': statusTheme === 'blue',
									'bg-red-100 text-red-800 border-red-200': statusTheme === 'red',
									'bg-orange-100 text-orange-800 border-orange-200': statusTheme === 'orange'
								}"
							>
								{{ submissionResource.doc?.status }}
							</div>
							<Button 
								@click="submitAssignment()"
								class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-md hover:shadow-lg transition-all duration-200 px-4 h-9 rounded-lg text-sm font-medium border-0"
							>
								<!-- <template #prefix>
									<Plus class="w-4 h-4" />
								</template> -->
								{{ __('Save') }}
							</Button>
						</div>
					</div>
					<!-- Success Message -->
					<div
						v-if="
							submissionName != 'new' &&
							!['Pass', 'Fail'].includes(submissionResource.doc?.status) &&
							submissionResource.doc?.owner == user.data?.name
						"
						class="bg-orange-50 border border-orange-200 text-[#ed8e22] p-4 rounded-xl leading-relaxed text-sm mb-6"
					>
						<div class="flex items-start space-x-3">
						<div class="w-5 h-5 text-[#ed8e22] mt-0.5">
							<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<div class="flex-1">
								<p class="font-medium mb-1">{{ __("Submission Received!") }}</p>
								<p class="mb-2">{{ __("Your assignment has been successfully submitted.") }}</p>
								<p class="text-[#d47a1a]">
									{{ __("Once graded by your instructor, you'll see the results here.") }}
									{{ __('You can still make edits if needed.') }}
								</p>
							</div>
						</div>
					</div>
					<!-- File Upload Section -->
					<div v-if="showUploader()" class="space-y-4">
						<div class="flex items-center space-x-2 mb-3">
							<svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
							</svg>
							<span class="text-sm font-medium text-gray-700">
								{{ __('Upload your assignment as {0}').format(assignment.data.type) }}
							</span>
						</div>
						
						<FileUploader
							v-if="!submissionFile"
							:fileTypes="getType()"
							:validateFile="validateFile"
							@success="(file) => saveSubmission(file)"
						>
							<template #default="{ uploading, progress, openFileSelector }">
								<div 
									@click="openFileSelector"
									class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 hover:bg-blue-50/50 transition-all duration-200 cursor-pointer group"
								>
									<div class="space-y-3">
										<div class="w-12 h-12 mx-auto bg-blue-100 rounded-xl flex items-center justify-center group-hover:bg-blue-200 transition-colors duration-200">
											<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
											</svg>
										</div>
										<div>
											<p class="text-sm font-medium text-gray-900">
												{{
													uploading
														? __('Uploading... {0}%').format(progress)
														: __('Click to upload your file')
												}}
											</p>
											<p class="text-xs text-gray-500 mt-1">{{ assignment.data.type }} files only</p>
										</div>
									</div>
								</div>
							</template>
						</FileUploader>

						<!-- Uploaded File Display -->
						<div v-else class="bg-gray-50 rounded-xl p-4">
							<div class="flex items-center justify-between">
								<div class="flex items-center space-x-3">
									<div class="w-10 h-10 bg-white rounded-lg border border-gray-200 flex items-center justify-center">
										<FileText class="h-5 w-5 text-gray-600" />
									</div>
									<div>
										<a
											:href="submissionFile.file_url"
											target="_blank"
											class="block text-sm font-medium text-gray-900 hover:text-blue-600 transition-colors duration-200"
										>
											{{ submissionFile.file_name }}
										</a>
										<p class="text-xs text-gray-500 mt-1">
											{{ getFileSize(submissionFile.file_size) }}
										</p>
									</div>
								</div>
								<button
									v-if="canModifyAssignment"
									@click="removeSubmission()"
									class="w-8 h-8 bg-red-100 hover:bg-red-200 rounded-lg flex items-center justify-center transition-colors duration-200 group"
								>
									<X class="w-4 h-4 text-red-600 group-hover:text-red-700" />
								</button>
							</div>
						</div>
					</div>
					<!-- URL Input Section -->
					<div v-else-if="assignment.data.type == 'URL'" class="space-y-3">
						<div class="flex items-center space-x-2">
							<svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
							</svg>
							<label class="text-sm font-medium text-gray-700">{{ __('Enter a URL') }}</label>
						</div>
						<FormControl
							v-model="answer"
							type="text"
							:readonly="!canModifyAssignment"
							placeholder="https://example.com"
							class="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
						/>
					</div>

					<!-- Text Editor Section -->
					<div v-else class="space-y-3">
						<div class="flex items-center space-x-2">
							<svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
							</svg>
							<label class="text-sm font-medium text-gray-700">{{ __('Write your answer') }}</label>
						</div>
						<div class="bg-white rounded-lg border border-gray-300 overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
							<TextEditor
								:content="answer"
								@change="(val) => (answer = val)"
								:editable="canModifyAssignment"
								:fixedMenu="true"
								editorClass="prose-sm max-w-none bg-white rounded-lg py-3 px-4 min-h-[8rem] focus:outline-none"
							/>
						</div>
					</div>
				</div>

				<!-- Evaluator Comments -->
				<div
					v-if="
						user.data?.name == submissionResource.doc?.owner &&
						submissionResource.doc?.comments
					"
					class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 space-y-4"
				>
					<div class="flex items-center space-x-2">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
							</svg>
						</div>
						<h4 class="text-lg font-semibold text-gray-900">{{ __('Instructor Feedback') }}</h4>
					</div>
					<div
						class="prose prose-sm max-w-none text-gray-700 leading-relaxed bg-gray-50 rounded-lg p-4"
						v-html="submissionResource.doc.comments"
					></div>
				</div>

				<!-- Skills Assessment -->
				<div v-if="canGradeSubmission" class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 space-y-6">
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-2">
							<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
								<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
								</svg>
							</div>
							<h4 class="text-lg font-semibold text-gray-900">{{ __('Skills Assessment') }}</h4>
						</div>
						<Button
							@click="showSkillModal = true"
							class="w-16 h-16 rounded-full !bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-md hover:shadow-lg transition-all duration-200 flex items-center justify-center p-0 border-0"
						>
							<Plus class="w-6 h-6" />
						</Button>
					</div>
					<div v-if="skillsResource.data?.length" class="space-y-4">
						<div 
							v-for="skill in skillsResource.data" 
							:key="skill.name"
							class="bg-gray-50 rounded-lg p-4 border border-gray-100 hover:border-gray-200 transition-colors duration-200"
						>
							<!-- Desktop Layout: Horizontal -->
							<div class="hidden md:flex items-center justify-between">
								<div class="flex-1">
									<div class="text-sm font-semibold text-gray-900 mb-1">
										{{ skill.data || skill.name }}
									</div>
									<div class="text-xs text-gray-600">
										{{ skill.description || 'No description provided' }}
									</div>
								</div>
								<div class="ml-6 flex items-center space-x-3">
									<!-- Stars or N/A display -->
									<div v-if="skillScores[skill.name] === 'N/A'" class="flex items-center">
										<span class="text-gray-400 font-mono text-base tracking-wider"> - - - - - </span>
									</div>
									<div v-else class="flex items-center space-x-1">
										<button
											v-for="star in 5"
											:key="star"
											@click="setSkillScore(skill.name, star)"
											@mouseenter="hoverStar = { skill: skill.name, star: star }"
											@mouseleave="hoverStar = null"
											class="p-1 rounded-lg transition-all duration-200 hover:bg-white hover:shadow-sm"
											type="button"
										>
											<Star
												:size="18"
												:class="[
													'transition-all duration-200',
													isStarFilled(skill.name, star) 
														? 'fill-[#ed8e22] stroke-[#ed8e22] text-[#ed8e22]' 
														: 'stroke-gray-300 hover:stroke-[#ed8e22] text-gray-300 hover:text-[#ed8e22]'
												]"
											/>
										</button>
									</div>
									
									<!-- Score display -->
									<div class="min-w-[40px] text-center">
										<span class="text-xs font-medium text-gray-600 bg-white px-2 py-1 rounded-md border">
											{{ skillScores[skill.name] === 'N/A' ? 'N/A' : (skillScores[skill.name] || 0) + '/5' }}
										</span>
									</div>
									
									<!-- N/A toggle button -->
									<button
										@click="setSkillNotApplicable(skill.name)"
										:class="[
											'p-2 rounded-lg transition-all duration-200 border',
											skillScores[skill.name] === 'N/A' 
												? 'bg-green-100 text-green-700 border-green-200 hover:bg-green-200' 
												: 'bg-white text-gray-400 border-gray-200 hover:bg-red-50 hover:text-red-600 hover:border-red-200'
										]"
										type="button"
										:title="skillScores[skill.name] === 'N/A' ? __('Enable Rating') : __('Mark as Not Applicable')"
									>
										<Check v-if="skillScores[skill.name] === 'N/A'" class="w-4 h-4" />
										<Ban v-else class="w-4 h-4" />
									</button>
								</div>
							</div>

							<!-- Mobile Layout: Vertical Stack -->
							<div class="md:hidden space-y-3">
								<!-- Skill Name -->
								<div class="text-sm font-semibold text-gray-900">
									{{ skill.data || skill.name }}
								</div>
								
								<!-- Description -->
								<div class="text-xs text-gray-600 leading-relaxed">
									{{ skill.description || 'No description provided' }}
								</div>
								
								<!-- Stars and Controls -->
								<div class="flex items-center justify-between pt-2">
									<div class="flex items-center space-x-3">
										<!-- Stars or N/A display -->
										<div v-if="skillScores[skill.name] === 'N/A'" class="flex items-center">
											<span class="text-gray-400 font-mono text-sm tracking-wider"> - - - - - </span>
										</div>
										<div v-else class="flex items-center space-x-1">
											<button
												v-for="star in 5"
												:key="star"
												@click="setSkillScore(skill.name, star)"
												@mouseenter="hoverStar = { skill: skill.name, star: star }"
												@mouseleave="hoverStar = null"
												class="p-1 rounded-lg transition-all duration-200 hover:bg-white hover:shadow-sm"
												type="button"
											>
												<Star
													:size="16"
													:class="[
														'transition-all duration-200',
														isStarFilled(skill.name, star) 
															? 'fill-[#ed8e22] stroke-[#ed8e22] text-[#ed8e22]' 
															: 'stroke-gray-300 hover:stroke-[#ed8e22] text-gray-300 hover:text-[#ed8e22]'
													]"
												/>
											</button>
										</div>
										
										<!-- Score display -->
										<div class="text-center">
											<span class="text-xs font-medium text-gray-600 bg-white px-2 py-1 rounded-md border">
												{{ skillScores[skill.name] === 'N/A' ? 'N/A' : (skillScores[skill.name] || 0) + '/5' }}
											</span>
										</div>
									</div>
									
									<!-- N/A toggle button -->
									<button
										@click="setSkillNotApplicable(skill.name)"
										:class="[
											'p-1.5 rounded-lg transition-all duration-200 border',
											skillScores[skill.name] === 'N/A' 
												? 'bg-green-100 text-green-700 border-green-200 hover:bg-green-200' 
												: 'bg-white text-gray-400 border-gray-200 hover:bg-red-50 hover:text-red-600 hover:border-red-200'
										]"
										type="button"
										:title="skillScores[skill.name] === 'N/A' ? __('Enable Rating') : __('Mark as Not Applicable')"
									>
										<Check v-if="skillScores[skill.name] === 'N/A'" class="w-3 h-3" />
										<Ban v-else class="w-3 h-3" />
									</button>
								</div>
							</div>
						</div>
					</div>
					<div v-else class="text-center py-8">
						<div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
							<svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
							</svg>
						</div>
						<p class="text-sm text-gray-500 mb-2">{{ __('No skills available') }}</p>
						<p class="text-xs text-gray-400">{{ __('Click "Add Skill" to create one.') }}</p>
					</div>
				</div>

				<!-- Grading -->
				<div v-if="canGradeSubmission" class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 space-y-6">
					<div class="flex items-center space-x-2">
						<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
							<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
							</svg>
						</div>
						<h4 class="text-lg font-semibold text-gray-900">{{ __('Grading & Evaluation') }}</h4>
					</div>
					
					<div class="space-y-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Grade') }}</label>
							<FormControl
								v-if="submissionResource.doc"
								v-model="submissionResource.doc.status"
								type="select"
								:options="submissionStatusOptions"
								class="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
							/>
						</div>
						
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Instructor Comments') }}</label>
							<div class="bg-gray-50 rounded-lg border border-gray-300 overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
								<TextEditor
									:content="comments"
									@change="
										(val) => {
											comments = val
											isDirty = true
										}
									"
									:editable="true"
									:fixedMenu="true"
									editorClass="prose-sm max-w-none bg-gray-50 rounded-lg py-3 px-4 min-h-[8rem] focus:outline-none"
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Modern Add Skill Modal -->
	<Dialog 
		v-model="showSkillModal"
		:options="{
			title: __('Add New Skill'),
			size: 'md',
		}"
	>
		<template #body-content>
			<div class="space-y-6 p-2">
				<div class="text-center mb-6">
					<div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-[#ed8e22] to-[#d47a1a] rounded-full flex items-center justify-center">
						<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
						</svg>
					</div>
					<p class="text-gray-600 text-sm">Create a new skill to assess student performance</p>
				</div>
				
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Skill Name') }}</label>
						<FormControl
							v-model="newSkillName"
							type="text"
							placeholder="e.g., Problem Solving, Critical Thinking..."
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
					</div>
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Description') }}</label>
						<FormControl
							v-model="newSkillDescription"
							type="textarea"
							placeholder="Describe what this skill represents and how it should be evaluated..."
							:rows="3"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
					</div>
				</div>
			</div>
		</template>
		<template #actions>
			<div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
				<Button 
					variant="subtle" 
					@click="closeSkillModal"
					class="px-6 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors duration-200"
				>
					{{ __('Cancel') }}
				</Button>
				<Button 
					@click="createNewSkill"
					:disabled="!newSkillName"
					class="!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200 !outline-none focus:!outline-none focus:!ring-2 focus:!ring-[#ed8e22] focus:!ring-offset-2 disabled:!bg-gray-400 disabled:cursor-not-allowed"
				>
					<template #prefix>
						<Plus class="w-4 h-4" />
					</template>
					{{ __('Create Skill') }}
				</Button>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Badge,
	Button,
	call,
	createResource,
	createDocumentResource,
	FileUploader,
	FormControl,
	TextEditor,
	toast,
	Dialog,
} from 'frappe-ui'
import { computed, inject, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { FileText, X, Plus, Star, Ban, Check } from 'lucide-vue-next'
import { getFileSize } from '@/utils'
import { useRouter } from 'vue-router'

const submissionFile = ref(null)
const answer = ref(null)
const comments = ref(null)
const router = useRouter()
const user = inject('$user')
const isDirty = ref(false)
const showSkillModal = ref(false)
const newSkillName = ref('')
const newSkillDescription = ref('')
const hoverStar = ref(null)

// Skills assessment data
const skills = ref([])
const skillScores = ref({})

const props = defineProps({
	assignmentID: {
		type: String,
		required: true,
	},
	submissionName: {
		type: String,
		default: 'new',
	},
	showTitle: {
		type: Boolean,
		default: true,
	},
})

onMounted(() => {
	window.addEventListener('keydown', keyboardShortcut)
})

const keyboardShortcut = (e) => {
	if (e.key === 's' && (e.ctrlKey || e.metaKey)) {
		submitAssignment()
		e.preventDefault()
	}
}

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

const assignment = createResource({
	url: 'frappe.client.get',
	params: {
		doctype: 'LMS Assignment',
		name: props.assignmentID,
	},
	auto: true,
	onSuccess(data) {
		if (props.submissionName != 'new') {
			submissionResource.reload()
		}
		// Load skills after assignment is loaded
		skillsResource.reload()
	},
})

// Resource to fetch available skills
const skillsResource = createResource({
	url: 'frappe.client.get_list',
	params: {
		doctype: 'LMS Skills',
		fields: ['name', 'data', 'description'],
		limit_page_length: 100,
	},
	auto: false,
})


const createSkillResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Skills',
				data: values.data,
				description: values.description,
			}
		}
	},
	onSuccess() {
		toast.success(__('Skill created successfully'))
		skillsResource.reload()
		closeSkillModal()
	},
	onError(err) {
		toast.error(err.messages?.[0] || err)
	}
})

const newSubmission = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		let doc = {
			doctype: 'LMS Assignment Submission',
			assignment: props.assignmentID,
			member: user.data?.name,
			skills_score: getSkillsScoreForSubmission(),
		}
		if (showUploader()) {
			doc.assignment_attachment = submissionFile.value.file_url
		} else {
			doc.answer = answer.value
		}
		return {
			doc: doc,
		}
	},
})

const imageResource = createResource({
	url: 'lms.lms.api.get_file_info',
	makeParams(values) {
		return {
			file_url: values.image,
		}
	},
	auto: false,
	onSuccess(data) {
		submissionFile.value = data
	},
})

const submissionResource = createDocumentResource({
	doctype: 'LMS Assignment Submission',
	name: props.submissionName,
	onError(err) {
		toast.error(err.messages?.[0] || err)
	},
	auto: false,
	cache: [user.data?.name, props.assignmentID],
})

watch(submissionResource, () => {
	if (submissionResource.doc) {
		if (submissionResource.doc.assignment_attachment) {
			imageResource.reload({
				image: submissionResource.doc.assignment_attachment,
			})
		}
		if (submissionResource.doc.answer) {
			answer.value = submissionResource.doc.answer
		}
		if (submissionResource.doc.comments) {
			comments.value = submissionResource.doc.comments
		}
		// Load skills scores from child table
		if (submissionResource.doc.skills_score && submissionResource.doc.skills_score.length > 0) {
			skillScores.value = {}
			submissionResource.doc.skills_score.forEach(skillScore => {
				// Handle N/A values and numeric scores
				if (skillScore.score === 'N/A') {
					skillScores.value[skillScore.skill] = 'N/A'
				} else {
					skillScores.value[skillScore.skill] = parseInt(skillScore.score) || 0
				}
			})
		}
		if (submissionResource.isDirty) {
			isDirty.value = true
		} else if (showUploader() && !submissionFile.value) {
			isDirty.value = true
		} else if (!showUploader() && !answer.value) {
			isDirty.value = true
		} else {
			isDirty.value = false
		}
	}
})

watch(submissionFile, () => {
	if (props.submissionName == 'new' && submissionFile.value) {
		isDirty.value = true
	}
})

const submitAssignment = () => {
	if (props.submissionName != 'new') {
		let evaluator =
			submissionResource.doc && submissionResource.doc.owner != user.data?.name
				? user.data?.name
				: null

		submissionResource.setValue.submit(
			{
				...submissionResource.doc,
				assignment_attachment: submissionFile.value?.file_url,
				evaluator: evaluator,
				comments: comments.value,
				answer: answer.value,
				skills_score: getSkillsScoreForSubmission(),
			},
			{
				onSuccess(data) {
					toast.success(__('Changes saved successfully'))
				},
			}
		)
	} else {
		addNewSubmission()
	}
}

const addNewSubmission = () => {
	newSubmission.submit(
		{},
		{
			onSuccess(data) {
				toast.success(__('Assignment submitted successfully'))
				if (router.currentRoute.value.name == 'AssignmentSubmission') {
					router.push({
						name: 'AssignmentSubmission',
						params: {
							assignmentID: props.assignmentID,
							submissionName: data.name,
						},
						query: { fromLesson: router.currentRoute.value.query.fromLesson },
					})
				} else {
					markLessonProgress()
					router.go()
				}
				submissionResource.name = data.name
				submissionResource.reload()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const saveSubmission = (file) => {
	isDirty.value = true
	submissionFile.value = file
}

const markLessonProgress = () => {
	if (router.currentRoute.value.name == 'Lesson') {
		let courseName = router.currentRoute.value.params.courseName
		let chapterNumber = router.currentRoute.value.params.chapterNumber
		let lessonNumber = router.currentRoute.value.params.lessonNumber

		call('lms.lms.api.mark_lesson_progress', {
			course: courseName,
			chapter_number: chapterNumber,
			lesson_number: lessonNumber,
		})
	}
}

const getType = () => {
	const type = assignment.data?.type
	if (type == 'Image') {
		return ['image/*']
	} else if (type == 'Document') {
		return [
			'.doc',
			'.docx',
			'.xml',
			'application/msword',
			'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
		]
	} else if (type == 'PDF') {
		return ['.pdf']
	}
}

const validateFile = (file) => {
	let type = assignment.data?.type
	let extension = file.name.split('.').pop().toLowerCase()
	if (type == 'Image' && !['jpg', 'jpeg', 'png'].includes(extension)) {
		return 'Only image file is allowed.'
	} else if (
		type == 'Document' &&
		!['doc', 'docx', 'xml'].includes(extension)
	) {
		return 'Only document file is allowed.'
	} else if (type == 'PDF' && !['pdf'].includes(extension)) {
		return 'Only PDF file is allowed.'
	}
}

const removeSubmission = () => {
	isDirty.value = true
	submissionFile.value = null
}

const canGradeSubmission = computed(() => {
	return (
		(user.data?.is_moderator ||
			user.data?.is_evaluator ||
			user.data?.is_instructor) &&
		props.submissionName != 'new' &&
		router.currentRoute.value.name == 'AssignmentSubmission'
	)
})

const canModifyAssignment = computed(() => {
	return (
		!submissionResource.doc ||
		(submissionResource.doc?.owner == user.data?.name &&
			submissionResource.doc?.status == 'Not Graded')
	)
})

const submissionStatusOptions = computed(() => {
	return [
		{ label: 'Not Graded', value: 'Not Graded' },
		{ label: 'Pass', value: 'Pass' },
		{ label: 'Fail', value: 'Fail' },
	]
})

const statusTheme = computed(() => {
	if (!submissionResource.doc) {
		return 'orange'
	} else if (submissionResource.doc.status == 'Pass') {
		return 'green'
	} else if (submissionResource.doc.status == 'Not Graded') {
		return 'blue'
	} else {
		return 'red'
	}
})

const showUploader = () => {
	return ['PDF', 'Image', 'Document'].includes(assignment.data?.type)
}

// Helper method to format skills score for submission
const getSkillsScoreForSubmission = () => {
	const scores = []
	if (skillsResource.data) {
		skillsResource.data.forEach(skill => {
			if (skillScores.value[skill.name] !== undefined) {
				scores.push({
					skill: skill.name,
					score: String(skillScores.value[skill.name]) // Keep as string (N/A or number)
				})
			}
		})
	}
	return scores
}

// Star rating methods
const setSkillScore = (skillName, score) => {
	skillScores.value[skillName] = score
	isDirty.value = true
}

const setSkillNotApplicable = (skillName) => {
	// Toggle between N/A and 0 (default state)
	if (skillScores.value[skillName] === 'N/A') {
		skillScores.value[skillName] = 0
	} else {
		skillScores.value[skillName] = 'N/A'
	}
	
	isDirty.value = true
	// Clear hover state if it's for this skill
	if (hoverStar.value && hoverStar.value.skill === skillName) {
		hoverStar.value = null
	}
}

const isStarFilled = (skillName, starNumber) => {
	// Don't show filled stars if skill is marked as N/A
	if (skillScores.value[skillName] === 'N/A') {
		return false
	}
	
	const currentScore = hoverStar.value && hoverStar.value.skill === skillName 
		? hoverStar.value.star 
		: (skillScores.value[skillName] || 0)
	return starNumber <= currentScore
}

// Modal methods
const createNewSkill = () => {
	if (newSkillName.value) {
		createSkillResource.submit({
			data: newSkillName.value,
			description: newSkillDescription.value
		})
	}
}

const closeSkillModal = () => {
	showSkillModal.value = false
	newSkillName.value = ''
	newSkillDescription.value = ''
}
</script>
